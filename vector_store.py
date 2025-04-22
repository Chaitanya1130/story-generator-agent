import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

load_dotenv()

class VectorStore:
    def __init__(self, collection_name: str = "story_knowledge_base"):
        self.collection_name = collection_name
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Initialize Qdrant client
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        if self.qdrant_url:
            self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        else:
            # Use local Qdrant instance
            self.client = QdrantClient(":memory:")
        
        # Create collection if it doesn't exist
        self._create_collection()
    
    def _create_collection(self):
        """Create a collection if it doesn't exist"""
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.encoder.get_sentence_embedding_dimension(),
                    distance=models.Distance.COSINE
                )
            )
    
    def add_texts(self, texts: List[str], metadata: List[Dict[str, Any]] = None):
        """Add texts to the vector store with optional metadata"""
        if metadata is None:
            metadata = [{}] * len(texts)
        
        vectors = self.encoder.encode(texts).tolist()
        
        # Prepare points for insertion
        points = [
            models.PointStruct(
                id=i,
                vector=vector,
                payload={"text": text, **meta}
            )
            for i, (vector, text, meta) in enumerate(zip(vectors, texts, metadata))
        ]
        
        # Insert points
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar texts based on the query"""
        query_vector = self.encoder.encode(query).tolist()
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        
        return [
            {
                "text": result.payload.get("text", ""),
                "score": result.score,
                **{k: v for k, v in result.payload.items() if k != "text"}
            }
            for result in results
        ] 