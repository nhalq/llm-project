from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessage

DEFAULT_SYSTEM_PROMPT = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question in vietnamese.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise."""

DEFAULT_HUMAN_PROMPT = """
Question: {question}
Context: {context}
Answer:"""


def create():
    system = SystemMessage(content=DEFAULT_SYSTEM_PROMPT)
    human = HumanMessagePromptTemplate.from_template(DEFAULT_HUMAN_PROMPT)
    prompt = ChatPromptTemplate.from_messages((system, human))
    return prompt
