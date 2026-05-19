from langchain_core.embeddings import Embeddings
import requests



class JinaEmbeddings(Embeddings):
    def __init__(self, api_key: str, model: str = "jina-embeddings-v3"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.jina.ai/v1/embeddings"

    def _embed(self, texts: list[str]) -> list[list[float]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"input": texts, "model": self.model}
        resp = requests.post(self.url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return [item["embedding"] for item in data["data"]]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts)

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text])[0]
