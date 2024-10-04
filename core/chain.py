from functools import lru_cache
from pymongo import MongoClient
from core.llm import create as create_llm
from core.prompt import create as create_prompt
from pymongo.errors import OperationFailure
from langchain_core.runnables import RunnablePassthrough
from fastapi import HTTPException
from typing import List
from core.store import KnowledgeStore 
from langchain.schema import BaseMessage

MONGODB_ATLAS_URI = "mongodb+srv://minhtri171997:test123@cluster0.vv0ot.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_ATLAS_URI)
db = client['llm_db'] 
collection = db['llm_collection']  

@lru_cache(maxsize=8)
def get_rag_chain(knowledge_domain: str):
    query = {"metadata.keywords": knowledge_domain}  
    try:
        mongo_documents = collection.find(query)
        knowledge_data = [doc.get('text') for doc in mongo_documents if doc.get('text')]
        return RAGInferenceChain(knowledge_data)
    except OperationFailure as e:
        raise HTTPException(status_code=500, detail=f"MongoDB query failed: {str(e)}")

class RAGInferenceChain:
    def __init__(self, knowledge_data):
        self.knowledge_data = knowledge_data
        self.llm = create_llm()
        self.store = KnowledgeStore() 

    def __call__(self, user_prompt: str, messages: List[BaseMessage] = []) -> str:
        context = self.retrieve(user_prompt)
        print(f" context : {type(context)}")
        prompt = create_prompt(messages=messages)
        rag_chain = (
            {"context": lambda x: context, "question": RunnablePassthrough()} | prompt | self.llm
        )

        ai_message = rag_chain.invoke(user_prompt)
        return ai_message

    def retrieve(self, query: str) -> str:
        return self.store.retrieve(query) 
