from enum import Enum

from app.config.pydantic import Immutable


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatGPTMessage(Immutable):
    role: Role
    content: str


class Choice(Immutable):
    index: int
    message: ChatGPTMessage


class ChatCompletion(Immutable):
    choices: list[Choice]
