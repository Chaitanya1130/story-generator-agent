import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

load_dotenv()

class VectorStore:
    def __init__(self, collection_name: str = "story_knowledge_base"):
        self.collection_name = collection_name
        self._encoder = None
        
        # Get Qdrant settings
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        # Initialize QdrantClient correctly
        if self.qdrant_url and self.qdrant_api_key:
            self.client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key
            )
        elif self.qdrant_url:
            self.client = QdrantClient(url=self.qdrant_url)
        else:
            self.client = QdrantClient(":memory:")
            
        self._create_collection()
    
    @property
    def encoder(self):
        if self._encoder is None:
            self._encoder = SentenceTransformer("all-MiniLM-L6-v2")
        return self._encoder
    
    def _create_collection(self):
        """Create collection if it doesn't exist"""
        try:
            existing = self.client.get_collections().collections
            existing_names = [c.name for c in existing]
            if self.collection_name not in existing_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.encoder.get_sentence_embedding_dimension(),
                        distance=models.Distance.COSINE
                    )
                )
        except Exception as e:
            print(f"Error creating collection: {e}")
    
    def add_texts(self, texts: List[str], metadata: Optional[List[Dict[str, Any]]] = None):
        """Add texts with optional metadata to the vector store"""
        if not texts:
            return
            
        if metadata is None:
            metadata = [{}] * len(texts)
        
        try:
            vectors = self.encoder.encode(texts).tolist()
            points = []
            
            for i, (vector, text, meta) in enumerate(zip(vectors, texts, metadata)):
                # Generate a unique ID for each point
                point_id = i + len(self.client.scroll(
                    collection_name=self.collection_name, 
                    limit=1
                )[0])
                
                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={"text": text, **(meta or {})}
                    )
                )
            
            if points:
                self.client.upsert(collection_name=self.collection_name, points=points)
        except Exception as e:
            print(f"Error adding texts to vector store: {e}")
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar texts in the vector store"""
        try:
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
        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []