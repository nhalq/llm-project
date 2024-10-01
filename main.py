__version__ = '0.1'
__description__ = 'LLM Project - Chatbot API'

from collections import defaultdict
from core.chain import RAGInferenceChain
from fastapi import FastAPI
from functools import lru_cache
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import dotenv
dotenv.load_dotenv()


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


@lru_cache(maxsize=8)
def get_rag_chain(knowledge_domain: str):
    return RAGInferenceChain(knowledge_domain)


app = FastAPI(version=__version__, description=__description__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

prepare_domain = ['thanhnien.vn']
for domain in prepare_domain:
    get_rag_chain(domain)
store: list[BaseMessage] = defaultdict(list)


@app.get('/')
def description() -> APIDescriptionResponseDTO:
    return APIDescriptionResponseDTO()


@app.get('/c/{uuid}')
def get_conversation(uuid: str) -> ConversationResponseDTO:
    def message_to_dto(message: BaseMessage) -> MessageDTO:
        return MessageDTO(role=message.type, message=message.content)

    conversation = map(message_to_dto, store[uuid])
    return ConversationResponseDTO(conversation=conversation)


@app.post('/c/{uuid}/ask')
def ask_chatbot(uuid: str, ask_dto: ChatbotAskRequestDTO) -> ChatbotAskResponseDTO:
    user_message = ask_dto.message
    store[uuid].append(HumanMessage(content=user_message))

    knowledge_domain = 'thanhnien.vn'
    chain = get_rag_chain(knowledge_domain)

    ai_message = chain(user_message, store)
    store[uuid].append(AIMessage(content=ai_message))

    return ChatbotAskResponseDTO(message=ai_message)
