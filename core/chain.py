import core.store
import core.llm
import core.prompt

from typing import *
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import BaseMessage
from langchain_core.runnables import RunnablePassthrough


class RAGInferenceChain:
    def __init__(self, knowledge_domain: str) -> None:
        self.vector_store = core.store.bind(knowledge_domain)
        self.llm = core.llm.create()

    @staticmethod
    def aggerate_documents(documents: List[Document]):
        return '\n\n'.join([document.page_content for document in documents])

    def retrive(self, user_prompt: str):
        retriver = self.vector_store.as_retriever()
        return retriver.invoke(user_prompt)

    def __call__(self, user_prompt: str, messages: List[BaseMessage] = []):
        prompt = core.prompt.create(messages=messages)
        params = dict({
            "context": self.vector_store.as_retriever() | self.aggerate_documents,
            "question": RunnablePassthrough()
        })

        chain = (params
                 | prompt
                 | self.llm
                 | StrOutputParser())

        ai_message = chain.invoke(user_prompt)
        return ai_message
