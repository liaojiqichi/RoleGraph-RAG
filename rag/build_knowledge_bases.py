import os
import json
import networkx as nx
import chromadb
from chromadb.utils import embedding_functions

GRAPH_JSON_PATH = os.getenv("GRAPH_JSON_PATH", "./kg_optimized.json")
GRAPH_OUTPUT_PATH = os.getenv("GRAPH_OUTPUT_PATH", "./mutsumi_graph.graphml")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

def build_knowledge_bases(json_filepath=GRAPH_JSON_PATH):
    print("1. Loading optimized knowledge graph JSON...")
    if not os.path.exists(json_filepath):
        print(f"Error: {json_filepath} not found!")
        return

    with open(json_filepath, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])
    print(f"Loaded {len(nodes)} nodes and {len(edges)} edges.")

    print("\n2. Building NetworkX Graph...")
    G = nx.DiGraph()

    for node in nodes:
        node = dict(node)
        node_id = node.pop("id")
        for k, v in node.items():
            if isinstance(v, list):
                node[k] = ", ".join(v)
        G.add_node(node_id, **node)

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        relation = edge.get("relation")
        if source and target:
            G.add_edge(source, target, relation=relation)

    nx.write_graphml(G, GRAPH_OUTPUT_PATH)
    print(f"Graph saved to {GRAPH_OUTPUT_PATH}")

    print("\n3. Building ChromaDB Vector Database...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    try:
        chroma_client.delete_collection("mutsumi_knowledge")
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name="mutsumi_knowledge",
        embedding_function=sentence_transformer_ef
    )

    documents, metadatas, ids = [], [], []

    for i, edge in enumerate(edges):
        source = edge.get("source")
        target = edge.get("target")
        relation = str(edge.get("relation")).replace("_", " ")

        if not source or not target:
            continue

        documents.append(f"{source} {relation} {target}.")
        metadatas.append({
            "source_node": str(source),
            "target_node": str(target),
            "type": "edge"
        })
        ids.append(f"edge_{i}")

    for i, node in enumerate(graph_data.get("nodes", [])):
        node_id = node.get("id")
        if not node_id:
            continue

        attributes = {k: v for k, v in node.items() if k != "id"}
        if attributes:
            attr_strings = [f"{k.replace('_', ' ')}: {v}" for k, v in attributes.items()]
            documents.append(f"Profile of {node_id}: " + "; ".join(attr_strings) + ".")
            metadatas.append({
                "source_node": str(node_id),
                "type": "node_profile"
            })
            ids.append(f"node_profile_{i}")

    batch_size = 100
    for i in range(0, len(documents), batch_size):
        collection.add(
            documents=documents[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size],
            ids=ids[i:i + batch_size]
        )

if __name__ == "__main__":
    build_knowledge_bases()