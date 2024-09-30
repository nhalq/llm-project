from typing import List
from langchain_core.prompts.chat import *


SYSTEM_PROMT = """Bạn là một trợ lý thực hiện các tác vụ trả lời câu hỏi.
Sử dụng các mẩu thông tin được cho dưới đây để trả lời câu hỏi của người dùng.
Nếu bạn không biết câu trả lời, phải trả lời rằng bạn không biết.
Chỉ được phép sử dụng tiếng Việt và giữ câu trả lời ngắn gọn nhất có thể.

Thông tin liên quan:
{context}"""

HUMAN_PROMPT = """{question}"""


def create(messages: List[BaseMessage] = []):
    system = SystemMessagePromptTemplate.from_template(SYSTEM_PROMT)
    human = HumanMessagePromptTemplate.from_template(HUMAN_PROMPT)

    prompt = ChatPromptTemplate.from_messages((system, *messages, human))
    return prompt
