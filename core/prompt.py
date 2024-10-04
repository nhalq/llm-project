from typing import List
from langchain_core.prompts.chat import *


SYSTEM_PROMT = """Bạn là một trợ lý thực hiện các tác vụ trả lời câu hỏi.
Chỉ được sử dụng các mẩu thông tin được cho dưới đây để trả lời câu hỏi của người dùng.
Nếu bạn không biết câu trả lời, phải trả lời rằng bạn không biết.
Giữ câu trả lời ngắn gọn nhất có thể và kèm theo đường dẫn (link) tới bài viết nếu có.

Thông tin liên quan:
{context}"""

HUMAN_PROMPT = """Trả lời câu hỏi sau hoàn toàn bằng tiếng Việt:
{question}"""


def create(messages: List[BaseMessage] = []):
    system = SystemMessagePromptTemplate.from_template(SYSTEM_PROMT)
    human = HumanMessagePromptTemplate.from_template(HUMAN_PROMPT)

    prompt = ChatPromptTemplate.from_messages((system, *messages, human))
    return prompt
