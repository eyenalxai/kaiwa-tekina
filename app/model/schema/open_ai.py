from enum import Enum

from app.config.pydantic import Immutable


class Role(str, Enum):  # noqa: WPS600 Found subclassing a builtin: str
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatGPTMessage(Immutable):
    role: Role
    content: str


class Choice(Immutable):
    index: int
    message: ChatGPTMessage


class Usage(Immutable):
    total_tokens: int


class ChatCompletion(Immutable):
    choices: list[Choice]
    usage: Usage


class ChatError(Immutable):
    message: str


class OpenAIError(Immutable):
    error: ChatError
