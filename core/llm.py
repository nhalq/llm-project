import os

from langchain_groq import ChatGroq


def create():
    llm = ChatGroq(api_key=os.getenv('LLM_API_KEY'),
                   model='llama3-8b-8192')
    return llm
