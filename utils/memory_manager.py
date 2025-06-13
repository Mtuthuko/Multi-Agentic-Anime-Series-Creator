# utils/memory_manager.py
import chromadb
from chromadb.utils import embedding_functions

class MemoryManager:
    def __init__(self, collection_name="anime_series_memory"):
        self.client = chromadb.Client()
        # Using a default sentence transformer model for embeddings
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    def add_episode_summary(self, episode_id: int, summary: str):
        """Adds an episode summary to the memory."""
        self.collection.add(
            documents=[summary],
            metadatas=[{"episode": episode_id}],
            ids=[f"ep_{episode_id}"]
        )
        print(f"Memory: Added summary for Episode {episode_id}.")

    def get_relevant_context(self, query: str, n_results: int = 3) -> str:
        """Queries the memory for context relevant to the query."""
        if self.collection.count() == 0:
            return "This is the first episode. There is no prior context."
            
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count())
        )
        context = "\n".join(results['documents'][0])
        print(f"Memory: Retrieved context - {context}")
        return context