import networkx as nx
import chromadb
from chromadb.utils import embedding_functions

class HybridRetriever:
    def __init__(self, db_path="./chroma_db", graph_path="./mutsumi_graph.graphml"):
        print("Loading Knowledge Bases...")
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="BAAI/bge-small-en-v1.5"
        )
        self.collection = self.chroma_client.get_collection(
            name="mutsumi_knowledge",
            embedding_function=self.embedding_fn
        )
        self.graph = nx.read_graphml(graph_path)
        print("Knowledge Bases Loaded Successfully!")

    def retrieve(self, query: str, top_k: int = 3, distance_threshold: float = 0.5):
        print("[Retriever] before collection.query")
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        print("[Retriever] after collection.query")

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        print("[Retriever] distances:", distances)

        if len(distances) == 0 or distances[0] > distance_threshold:
            print("[Retriever] out of scope")
            return "[OUT_OF_SCOPE]", []

        entry_nodes = set()
        context_parts = ["=== Direct Memory Retrieval ==="]

        for doc, meta, dist in zip(documents, metadatas, distances):
            if dist <= distance_threshold:
                context_parts.append(f"- {doc}")
                if "source_node" in meta:
                    entry_nodes.add(meta["source_node"])
                if "target_node" in meta:
                    entry_nodes.add(meta["target_node"])

        print("[Retriever] before graph expansion")
        context_parts.append("\n=== Graph-Expanded Memory (1-hop) ===")
        expanded_facts = set()

        for node in entry_nodes:
            if self.graph.has_node(node):
                node_data = self.graph.nodes[node]
                profile = ", ".join([f"{k}:{v}" for k, v in node_data.items() if k != "id"])
                if profile:
                    expanded_facts.add(f"Profile of {node}: {profile}")

                for neighbor in self.graph.successors(node):
                    edge_data = self.graph.get_edge_data(node, neighbor)
                    relation = edge_data.get("relation", "related to").replace("_", " ")
                    expanded_facts.add(f"- Fact: {node} {relation} {neighbor}.")

                for neighbor in self.graph.predecessors(node):
                    edge_data = self.graph.get_edge_data(neighbor, node)
                    relation = edge_data.get("relation", "related to").replace("_", " ")
                    expanded_facts.add(f"- Fact: {neighbor} {relation} {node}.")

        print("[Retriever] after graph expansion")
        final_context = "\n".join(context_parts + list(expanded_facts)[:10])
        return final_context, list(entry_nodes)

# retriever = HybridRetriever()
#
# test_queries = [
#     "Who is Sakiko?",
#     "Why did you give Soyo cucumbers?",
#     "What do you think about the iPhone 15?",
# ]
#
# print("\n" + "="*50)
# for q in test_queries:
#     print(f" User Query: {q}")
#     context, nodes = retriever.retrieve(q, top_k=3)
#     if context == "[OUT_OF_SCOPE]":
#         print("System:[OUT_OF_SCOPE] -> The character does not know about this.")
#     else:
#         print(f"Entry Nodes Found: {nodes}")
#         print(f"Retrieved Context:\n{context}")
#     print("="*50)
