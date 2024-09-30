from langchain_groq import ChatGroq


def create():
    llm = ChatGroq(model='llama3-8b-8192')
    return llm
