import os
import json
import torch
from pathlib import Path
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import HfFolder


class KnowledgeBase:
    def __init__(self, embedding_model="intfloat/e5-large-v2"):
        self.documents = []
        self.metadata = []
        self.embeddings = None
        self.embedding_model = SentenceTransformer(embedding_model)

    def process_directory(self, data_dir: str) -> None:
        """Load and process multiple restaurant JSON files."""
        all_docs, all_meta = [], []
        for file_name in os.listdir(data_dir):
            if file_name.endswith(".json"):
                with open(os.path.join(data_dir, file_name), "r") as f:
                    data = json.load(f)
                    chunks = self._create_chunks(data)
                    all_docs.extend(chunks["chunks"])
                    all_meta.extend(chunks["metadata"])
        self.documents = all_docs
        self.metadata = all_meta
        self.embeddings = self.embedding_model.encode(self.documents, convert_to_tensor=True)

    def _create_chunks(self, restaurant: Dict[str, Any]) -> Dict[str, List]:
        chunks, metadata = [], []
        name = restaurant.get("restaurant_name", "Unknown")

        # Basic Info
        info = f"Restaurant: {name}\nLocation: {restaurant.get('location', 'Unknown')}\n"
        info += f"Operating Hours: {restaurant.get('operating_hours', 'Unknown')}\n"
        contact = restaurant.get("contact_info", {})
        if contact:
            info += "Contact Info:\n" + "\n".join([f"- {k}: {v}" for k, v in contact.items()]) + "\n"
        if restaurant.get("special_features"):
            info += f"Special Features: {restaurant['special_features']}\n"
        chunks.append(info)
        metadata.append({"restaurant": name, "type": "basic"})

        # Menu
        items = restaurant.get("menu_items", [])
        for i in range(0, len(items), 5):
            part = items[i:i + 5]
            text = f"Menu for {name} (Part {i//5 + 1}):\n"
            for item in part:
                text += f"- {item.get('name')}: {item.get('description', '')} Price: {item.get('price', '')}\n"
            chunks.append(text)
            metadata.append({"restaurant": name, "type": "menu", "part": i//5 + 1})

        # Reviews
        reviews = restaurant.get("reviews", [])
        if reviews:
            text = f"Reviews for {name}:\n"
            for r in reviews[:5]:
                text += f"Rating: {r.get('star_rating')} - {r.get('comment')} (by {r.get('reviewer_name')})\n"
            chunks.append(text)
            metadata.append({"restaurant": name, "type": "reviews"})

        return {"chunks": chunks, "metadata": metadata}

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        if not self.documents or self.embeddings is None:
            raise ValueError("Knowledge base is empty.")
        query_embedding = self.embedding_model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]
        top_results = torch.topk(cos_scores, k=min(k, len(cos_scores)))
        results = []
        for score, idx in zip(top_results[0], top_results[1]):
            results.append({
                "text": self.documents[idx],
                "metadata": self.metadata[idx],
                "score": float(score)
            })
        return results


class RestaurantRAG:
    def __init__(self, data_dir: str, llm_model="google/gemma-2-2b-it"):
        self.kb = KnowledgeBase()
        print("[+] Loading and processing restaurant data...")
        self.kb.process_directory(data_dir)

        print(f"[+] Loading LLM model: {llm_model}")
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model)
        self.model = AutoModelForCausalLM.from_pretrained(
            llm_model,
            device_map="auto",
            torch_dtype=torch.bfloat16
        )

    def answer_query(self, query: str, top_k: int = 5) -> str:
        print(f"[?] Searching for: {query}")
        relevant_chunks = self.kb.search(query, k=top_k)
        context = "\n\n".join([doc["text"] for doc in relevant_chunks])

        prompt = f"""You are a helpful restaurant assistant.
Answer the question using the information below. If not available, say "Not found".

Context:
{context}

Question: {query}
Answer:"""

        input_ids = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        output = self.model.generate(**input_ids, max_new_tokens=200)
        answer = self.tokenizer.decode(output[0], skip_special_tokens=True)

        return answer.split("Answer:")[-1].strip()


# === EXAMPLE USAGE ===
if __name__ == "__main__":
    data_path = r"C:\Users\ASUS\Desktop\zomato_assignment\zomato\zomato\data"
    chatbot = RestaurantRAG(data_path)

    print("\nType 'exit' to quit.\n")
    while True:
        user_query = input("Ask your restaurant query: ")
        if user_query.lower() in ("exit", "quit"):
            break
        response = chatbot.answer_query(user_query)
        print("\n💬", response, "\n")
