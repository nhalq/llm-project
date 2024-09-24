import core.embedding
from langchain_chroma import Chroma


def create(collection_name='vector_store'):
    vector_store = Chroma(collection_name=collection_name,
                          # persist_directory='data',
                          embedding_function=core.embedding.create())
    return vector_store
