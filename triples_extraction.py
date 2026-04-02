import os
import json
import re
import networkx as nx
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI
import spacy

load_dotenv()

API_KEY = ""
BASE_URL = "https://api.deepseek.com"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
MODEL_NAME = "deepseek-chat"

nlp = spacy.load("en_core_web_sm")

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def split_paragraphs(text):
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]

def extract_entities(sentence):
    doc = nlp(sentence)
    valid_labels = {"PERSON", "ORG", "GPE", "FAC", "LOC", "WORK_OF_ART"}
    return list(set([ent.text.strip() for ent in doc.ents if ent.label_ in valid_labels]))

def extract_triples(sentence):
    prompt = f"""
Extract ALL possible knowledge triples from the text.

Rules:
- Output ONLY a JSON list of dictionaries.
- Format:[{{"subject": "...", "relation": "...", "object": "...", "is_attribute": true/false}}]
- `is_attribute` MUST be true if the object is a literal value (like age, height, date, color, job title, description) describing the subject.
- `is_attribute` MUST be false if the object is another distinct entity (like a person, place, organization, item).
- Relations should be concise (e.g., "member_of", "plays", "wears", "age", "height").
- Clean up entities (e.g., remove "'s").
- Only extract explicit facts. If none, return[].

Text:
{sentence}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert knowledge extraction system."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()
        content = re.sub(r"^```json\s*", "", content)
        content = re.sub(r"^```\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        return json.loads(content.strip())

    except Exception as e:
        print("LLM error or JSON parse error:", e)
        return []

def normalize_entity(entity):
    if not isinstance(entity, str):
        return None

    entity = entity.strip()
    entity = re.sub(r"^(the|a|an)\s+", "", entity, flags=re.IGNORECASE)
    entity = re.sub(r"('s|:|;|,|\.|'|-)$", "", entity, flags=re.IGNORECASE).strip()

    ignore_list = {"first", "two", "days", "one", "three", "watashi", "i", "my", "me", "true", "others"}
    if entity.lower() in ignore_list or entity.isdigit() or len(entity) < 2:
        return None

    alias_map = {
        "Mutsumi": "Wakaba Mutsumi",
        "Mutsumi Chan": "Wakaba Mutsumi",
        "Tsukinomori school": "Tsukinomori Girls' Academy",
        "Tsukinomori": "Tsukinomori Girls' Academy",
        "Soyo": "Nagasaki Soyo",
        "Soyo Chan": "Nagasaki Soyo",
        "Sakiko": "Toyokawa Sakiko",
        "Sakiko Chan": "Toyokawa Sakiko",
        "Saki": "Toyokawa Sakiko",
        "Tomori": "Takamatsu Tomori",
        "Taki": "Shiina Taki",
        "Uika": "Misumi Uika",
        "Uika Chan": "Misumi Uika",
        "Nyamu": "Utenji Nyamu",
        "Nyamu Chan": "Utenji Nyamu",
        "Minami": "Minami Mori",
        "Minami Chan": "Minami Mori",
        "Umiri": "Yahata Umiri",
        "Umiri Chan": "Yahata Umiri"
    }

    return alias_map.get(entity, entity)

def build_graph(triples_list):
    G = nx.DiGraph()

    for triples in triples_list:
        for t in triples:
            try:
                raw_s = t.get("subject", "")
                raw_o = t.get("object", "")
                r = t.get("relation", "").strip().lower()
                is_attr = t.get("is_attribute", False)

                s = normalize_entity(raw_s)
                if not s:
                    continue

                if is_attr:
                    if not G.has_node(s):
                        G.add_node(s)
                    attr_key = r.replace(" ", "_")
                    G.nodes[s][attr_key] = raw_o
                else:
                    o = normalize_entity(raw_o)
                    if o and s != o:
                        G.add_node(s)
                        G.add_node(o)
                        G.add_edge(s, o, relation=r)

            except Exception:
                continue

    return G

def add_cooccurrence_edges(G, sentences):
    for sent in sentences:
        raw_entities = extract_entities(sent)
        entities = [normalize_entity(e) for e in raw_entities]
        entities = list(set([e for e in entities if e is not None]))

        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                e1, e2 = entities[i], entities[j]

                if e1 != e2 and G.has_node(e1) and G.has_node(e2):
                    if not G.has_edge(e1, e2) and not G.has_edge(e2, e1):
                        G.add_edge(e1, e2, relation="co_occurs")

    return G

def save_graph(G, path="kg_optimized.json"):
    data = nx.node_link_data(G)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def print_stats(G):
    print("\n===== Graph Stats =====")
    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    if G.number_of_nodes() > 0:
        avg_degree = G.number_of_edges() / G.number_of_nodes()
        print("Avg Degree:", round(avg_degree, 2))

    print("Connected Components:", nx.number_weakly_connected_components(G))

text = load_text("Truth about Wakaba Mutsumi.txt")

paragraphs = split_paragraphs(text)
print("Total paragraphs:", len(paragraphs))

all_triples = []

for sent in tqdm(paragraphs, desc="Extracting Triples"):
    triples = extract_triples(sent)
    if triples:
        all_triples.append(triples)

print("\nTotal triples extracted by LLM:", sum(len(t) for t in all_triples))

G = build_graph(all_triples)
G = add_cooccurrence_edges(G, paragraphs)

save_graph(G)
print_stats(G)
