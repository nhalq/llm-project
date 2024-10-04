from langchain_groq import ChatGroq
import os

os.environ["GROQ_API_KEY"] = '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'

def create():
    llm = ChatGroq(model='llama3-8b-8192')
    return llm
