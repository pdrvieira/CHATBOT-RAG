from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "BAAI/bge-small-en-v1.5"

_modelo = None  # guarda o modelo em memória


def get_embedding_model() -> SentenceTransformer:
    global _modelo
    if _modelo is None:
        _modelo = SentenceTransformer(MODEL_NAME)
    return _modelo


def gerar_embedding(texto: str) -> list[float]:
    modelo = get_embedding_model()
    embedding = modelo.encode(texto, normalize_embeddings=True)
    return embedding.tolist()


def calcular_similaridade(vec1: list[float], vec2: list[float]) -> float:
    # já vêm normalizados, então é só fazer dot product
    a = np.array(vec1)
    b = np.array(vec2)
    
    similaridade = np.dot(a, b)
    return float(similaridade)

