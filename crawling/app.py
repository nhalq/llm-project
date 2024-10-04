from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import numpy as np  # For handling vectors
from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain.embeddings import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')


MONGODB_ATLAS_URI = "mongodb+srv://minhtri171997:test123@cluster0.vv0ot.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_ATLAS_URI)
db = client['llm_db'] 
collection = db['llm_collection']  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

store = defaultdict(list)

class ChatbotAskRequestDTO(BaseModel):
    message: str

class ChatbotAskResponseDTO(BaseModel):
    message: str

class MessageDTO(BaseModel):
    role: str
    message: str

class ConversationResponseDTO(BaseModel):
    conversation: list[MessageDTO]

def compute_embedding(text: str) -> list:
    return embedding_model.embed_documents([text])[0]

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

    def __call__(self, query, conversation_history):
        response = self.retrieve_answer(query)
        return response

    def retrieve_answer(self, query):
        relevant_data = self.search_knowledge(query)
        if relevant_data:
            return relevant_data
        else:
            return f"Sorry, I could not find relevant information for the question: {query}"

    def search_knowledge(self, query):
        query_embedding = compute_embedding(query) 
        try:
            result = collection.aggregate([
                {
                    "$vectorSearch": {
                        "index": "vector_index",  
                        "path": "embedding",  
                        "queryVector": query_embedding, 
                        "numCandidates": 5, 
                        "limit": 5  
                    }
                },
                {
                    "$project": {
                        "text": 1,  
                        "score": {"$meta": "searchScore"}  
                    }
                }
            ])

            documents = list(result)
            if documents:
                return documents[0].get('text') 
            return None
        except OperationFailure as e:
            raise HTTPException(status_code=500, detail=f"MongoDB aggregation failed: {str(e)}")



@app.post('/c/{uuid}/ask')
def ask_chatbot(uuid: str, ask_dto: ChatbotAskRequestDTO) -> ChatbotAskResponseDTO:
    user_message = ask_dto.message
    store[uuid].append(HumanMessage(content=user_message))

    knowledge_domain = 'thời sự'  
    chain = get_rag_chain(knowledge_domain)  

    ai_message = chain(user_message, store[uuid])
    store[uuid].append(AIMessage(content=ai_message))

    return ChatbotAskResponseDTO(message=ai_message)


@app.get('/c/{uuid}')
def get_conversation(uuid: str) -> ConversationResponseDTO:
    def message_to_dto(message: BaseMessage) -> MessageDTO:
        return MessageDTO(role=message.type, message=message.content)

    conversation = list(map(message_to_dto, store[uuid]))
    return ConversationResponseDTO(conversation=conversation)
