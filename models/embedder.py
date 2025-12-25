# models/embedder.py
from sentence_transformers import SentenceTransformer
from config.settings import settings

class Embedder:
    """
    Handles text embedding using SentenceTransformer models.
    """
    def __init__(self):
        print(f"Loading embedding model: {settings.EMBED_MODEL}")
        self.model = SentenceTransformer(settings.EMBED_MODEL)

    def embed_texts(self, texts):
        """
        Embed multiple texts.
        
        Args:
            texts: List of text strings
        
        Returns:
            List of embedding vectors
        """
        return self.model.encode(
            texts, 
            show_progress_bar=True, 
            normalize_embeddings=True
        ).tolist()

    def embed_query(self, text):
        """
        Embed a single query text.
        
        Args:
            text: Query string
        
        Returns:
            Single embedding vector
        """
        return self.model.encode(
            [text], 
            normalize_embeddings=True
        ).tolist()[0]
