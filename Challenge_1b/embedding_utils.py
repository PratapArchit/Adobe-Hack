from sentence_transformers import SentenceTransformer

def load_model():
    """
    Loads a pre-trained MiniLM model from the local models directory.
    Ensure that ./models/all-MiniLM-L6-v2 is available in offline setup.
    """
    return SentenceTransformer("./models/all-MiniLM-L6-v2")

def get_embeddings(model, texts):
    """
    Generate embeddings for a list of texts using the loaded model.
    Returns a numpy array of embeddings.
    """
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
