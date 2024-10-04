from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from collections import defaultdict
from core.chain import RAGInferenceChain, get_rag_chain  # Importing from chain.py
from fastapi import FastAPI, HTTPException
from functools import lru_cache
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import dotenv

dotenv.load_dotenv()

MONGODB_ATLAS_URI = "mongodb+srv://minhtri171997:test123@cluster0.vv0ot.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_ATLAS_URI)
db = client['llm_db']
collection = db['llm_collection']

__version__ = '0.1'
__description__ = 'LLM Project - Chatbot API'

app = FastAPI(version=__version__, description=__description__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class APIDescriptionResponseDTO(BaseModel):
    name: str = 'llm-chatbot-api'
    version: str = __version__
    description: str = __description__

class ChatbotAskRequestDTO(BaseModel):
    message: str = 'Hello, how are you?'

class ChatbotAskResponseDTO(BaseModel):
    message: str = 'I\'m doing fine, thank you!'

class MessageDTO(BaseModel):
    role: str = 'user'
    message: str = 'Hello, how are you?'

class ConversationResponseDTO(BaseModel):
    conversation: list[MessageDTO]

# Store for conversation history
store: defaultdict = defaultdict(list)

@app.get('/')
def description() -> APIDescriptionResponseDTO:
    return APIDescriptionResponseDTO()

@app.get('/c/{uuid}')
def get_conversation(uuid: str) -> ConversationResponseDTO:
    def message_to_dto(message: BaseMessage) -> MessageDTO:
        return MessageDTO(role=message.type, message=message.content)

    conversation = list(map(message_to_dto, store[uuid]))
    return ConversationResponseDTO(conversation=conversation)

@app.post('/c/{uuid}/ask')
def ask_chatbot(uuid: str, ask_dto: ChatbotAskRequestDTO) -> ChatbotAskResponseDTO:
    user_message = ask_dto.message
    store[uuid].append(HumanMessage(content=user_message))
    chain = get_rag_chain(user_message) 
    try:
        ai_response = chain(user_message, store[uuid]) 
        
        print(f"ai_response: {ai_response}")

        if hasattr(ai_response, 'content'):
            ai_message = ai_response.content  
        else:
            raise ValueError("Unexpected response format from chain. 'content' attribute not found.")

        additional_info = ai_response.additional_kwargs 
        print(f"Additional Info: {additional_info}")

        store[uuid].append(AIMessage(content=ai_message))  

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  

    return ChatbotAskResponseDTO(message=ai_message)



