import core.embedding
from langchain_chroma import Chroma


def bind(collection_name: str, persist_directory: str = 'data'):
    embedding_function = core.embedding.create()
    vector_store = Chroma(collection_name=collection_name,
                          embedding_function=embedding_function,
                          persist_directory=persist_directory,)

    return vector_store
