import re
import networkx as nx
import chromadb
from chromadb.utils import embedding_functions


class HybridRetriever:

    def __init__(
        self,
        db_path="./chroma_db",
        graph_path="./mutsumi_graph.graphml"
    ):

        print("Loading Knowledge Bases...")

        self.chroma_client = chromadb.PersistentClient(path=db_path)

        self.embedding_fn = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="BAAI/bge-base-en-v1.5"
            )
        )

        self.collection = self.chroma_client.get_collection(
            name="mutsumi_knowledge",
            embedding_function=self.embedding_fn
        )

        self.graph = nx.read_graphml(graph_path)

        self.aliases = {
            "Sakiko": "Toyokawa Sakiko",
            "Mutsumi": "Wakaba Mutsumi",
            "Mortis": "Mortis",
            "Soyo": "Nagasaki Soyo",
            "Tomori": "Takamatsu Tomori",
            "Taki": "Shiina Taki",
            "Nyamu": "Utenji Nyamu",
            "Uika": "Misumi Uika",
            "Umiri": "Yahata Umiri",
        }

        self.attribute_aliases = {
            "hair color": "hair_color",
            "hair": "hair_color",
            "age": "age",
            "instrument": "plays_instrument",
            "play": "plays_instrument",
            "birthday": "birth_date",
            "birth date": "birth_date",
            "height": "height",
            "personality": "personality",
            "occupation": "occupation",
            "role": "role_in_band",
            "band": "member_of",
        }

        print("Knowledge Bases Loaded Successfully!")


    def resolve_entity(self, query):

        for alias, real_name in self.aliases.items():
            if alias.lower() in query.lower():
                return real_name

        return None

    def detect_attribute_query(self, query):

        query_lower = query.lower()

        for phrase, attr in self.attribute_aliases.items():
            if phrase in query_lower:
                return attr

        return None

    def structured_lookup(self, entity, attribute):

        if entity is None:
            return None

        if not self.graph.has_node(entity):
            return None

        node_data = self.graph.nodes[entity]

        if attribute in node_data:

            value = node_data[attribute]

            return f"{entity}'s {attribute.replace('_', ' ')} is {value}."

        relation_results = []

        for neighbor in self.graph.successors(entity):

            edge_data = self.graph.get_edge_data(entity, neighbor)

            relation = edge_data.get("relation", "")

            if relation == attribute:

                relation_results.append(neighbor)

        if relation_results:

            joined = ", ".join(relation_results)

            return f"{entity} {attribute.replace('_', ' ')} {joined}."

        return None

    def semantic_retrieve(
        self,
        query,
        top_k=3,
        distance_threshold=0.4
    ):

        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        if len(distances) == 0 or distances[0] > distance_threshold:
            return "[OUT_OF_SCOPE]", []

        entry_nodes = set()

        context_parts = [
            "=== Direct Memory Retrieval ==="
        ]

        for doc, meta, dist in zip(
            documents,
            metadatas,
            distances
        ):

            if dist <= distance_threshold:

                context_parts.append(
                    f"- {doc} (distance={dist:.3f})"
                )

                if "source_node" in meta:
                    entry_nodes.add(meta["source_node"])

                if "target_node" in meta:
                    entry_nodes.add(meta["target_node"])

        context_parts.append(
            "\n=== Graph-Expanded Memory (1-hop) ==="
        )

        expanded_facts = set()

        for node in entry_nodes:

            if not self.graph.has_node(node):
                continue

            node_data = self.graph.nodes[node]


            important_attrs = [
                "age",
                "personality",
                "hair_color",
                "role_in_band",
                "occupation",
            ]

            profile_parts = []

            for attr in important_attrs:

                if attr in node_data:

                    profile_parts.append(
                        f"{attr}:{node_data[attr]}"
                    )

            if profile_parts:

                expanded_facts.add(
                    f"Profile of {node}: "
                    + ", ".join(profile_parts)
                )

            for neighbor in list(
                self.graph.successors(node)
            )[:5]:

                edge_data = self.graph.get_edge_data(
                    node,
                    neighbor
                )

                relation = edge_data.get(
                    "relation",
                    "related to"
                ).replace("_", " ")

                expanded_facts.add(
                    f"- Fact: {node} {relation} {neighbor}."
                )

            for neighbor in list(
                self.graph.predecessors(node)
            )[:3]:

                edge_data = self.graph.get_edge_data(
                    neighbor,
                    node
                )

                relation = edge_data.get(
                    "relation",
                    "related to"
                ).replace("_", " ")

                expanded_facts.add(
                    f"- Fact: {neighbor} {relation} {node}."
                )

        for fact in list(expanded_facts)[:8]:
            context_parts.append(fact)

        final_context = "\n".join(context_parts)

        return final_context, list(entry_nodes)

    def retrieve(
        self,
        query,
        top_k=3,
        distance_threshold=0.5
    ):

        entity = self.resolve_entity(query)

        attribute = self.detect_attribute_query(query)

        if entity and attribute:

            structured_answer = self.structured_lookup(
                entity,
                attribute
            )

            if structured_answer:

                return (
                    "[STRUCTURED_RETRIEVAL]\n"
                    + structured_answer,
                    [entity]
                )

        return self.semantic_retrieve(
            query,
            top_k,
            distance_threshold
        )


if __name__ == "__main__":

    retriever = HybridRetriever()