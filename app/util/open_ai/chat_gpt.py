from collections.abc import Callable

from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession
from tiktoken import Encoding

from app.model.models import UserModel
from app.model.schema.open_ai import ChatCompletion, ChatGPTMessage, OpenAIError, Role
from app.util.messages import get_previous_messages
from app.util.open_ai.send_request import send_openai_request
from app.util.settings import shared_settings


def first_choice(chat_completion: ChatCompletion) -> ChatGPTMessage:
    return min(chat_completion.choices, key=lambda choice: choice.index).message


def token_reducer(
    messages: list[ChatGPTMessage],
    tokenizer: Encoding,
) -> list[ChatGPTMessage]:
    total_tokens = sum(len(tokenizer.encode(message.content)) for message in messages)

    while total_tokens > shared_settings.max_prompt_tokens:
        messages.pop(0)
        total_tokens = sum(
            len(tokenizer.encode(message.content)) for message in messages
        )

    return messages


def get_token_count_and_message(
    chat_completion: ChatCompletion,
) -> tuple[int, ChatGPTMessage]:
    return (
        chat_completion.usage.total_tokens,
        first_choice(chat_completion=chat_completion),
    )


ReturnType = ChatGPTMessage | OpenAIError


def chat_gpt_wrapper() -> Callable[[list[ChatGPTMessage]], tuple[int, ReturnType]]:
    url = shared_settings.openai_chat_api_url
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {openai_token}".format(
            openai_token=shared_settings.openai_token,
        ),
    }

    def chat_prompt(
        messages: list[ChatGPTMessage],
    ) -> tuple[int, ReturnType]:
        response, is_error = send_openai_request(
            url=url,
            headers=headers,
            messages=messages,
        )

        if is_error:
            return 0, OpenAIError(**response.json())

        chat_completion = ChatCompletion(**response.json())

        return get_token_count_and_message(chat_completion=chat_completion)

    return chat_prompt


def build_prompt(
    previous_messages: list[ChatGPTMessage],
    user_prompt: str,
    tokenizer: Encoding,
) -> list[ChatGPTMessage]:
    combined = [
        *previous_messages,
        ChatGPTMessage(
            role=Role.USER,
            content=user_prompt,
        ),
    ]

    return token_reducer(
        messages=combined,
        tokenizer=tokenizer,
    )


async def respond_to_chat_message(  # noqa: WPS211 Found too many arguments
    async_session: AsyncSession,
    fernet: Fernet,
    tokenizer: Encoding,
    user: UserModel,
    chat_prompt: Callable[[list[ChatGPTMessage]], tuple[int, ReturnType]],
    message_text: str,
) -> tuple[int, ReturnType]:
    previous_messages = await get_previous_messages(
        async_session=async_session,
        fernet=fernet,
        user=user,
    )

    prompt = build_prompt(
        previous_messages=previous_messages,
        tokenizer=tokenizer,
        user_prompt=message_text,
    )

    return chat_prompt(prompt)
