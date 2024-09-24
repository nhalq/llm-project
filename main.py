__version__ = '0.1'
__description__ = 'LLM Project - Chatbot API'

from fastapi import FastAPI
from pydantic import BaseModel

import core.llm
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


app = FastAPI(version=__version__, description=__description__)
llm = core.llm.create()
store = list()


@app.get('/')
def description() -> APIDescriptionResponseDTO:
    return APIDescriptionResponseDTO()


@app.get('/conversations')
def get_conversation() -> ConversationResponseDTO:
    return ConversationResponseDTO(conversation=store)


@app.put('/conversations/ask')
def ask_chatbot(ask_dto: ChatbotAskRequestDTO) -> ChatbotAskResponseDTO:
    user_message = ask_dto.message
    store.append(MessageDTO(role='user', message=user_message))

    assistant_message = llm.invoke(ask_dto.message).content
    store.append(MessageDTO(role='assistant', message=assistant_message))

    return ChatbotAskResponseDTO(message=assistant_message)
