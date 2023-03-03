from collections.abc import Callable

from app.model.schema.open_ai import ChatCompletion, ChatGPTMessage
from app.util.open_ai.send_request import send_openai_request
from app.util.settings import shared_settings


def first_choice(chat_completion: ChatCompletion) -> ChatGPTMessage:
    return min(chat_completion.choices, key=lambda choice: choice.index).message


def chat_gpt_wrapper() -> Callable[[list[ChatGPTMessage]], tuple[int, ChatGPTMessage]]:
    url = shared_settings.openai_chat_api_url
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {openai_token}".format(
            openai_token=shared_settings.openai_token,
        ),
    }
    configuration = {
        "model": "gpt-3.5-turbo",
    }

    def chat_prompt(messages: list[ChatGPTMessage]) -> tuple[int, ChatGPTMessage]:
        response = send_openai_request(
            url=url,
            headers=headers,
            configuration={**configuration},
            messages=messages,
        )

        chat_completion = ChatCompletion(**response.json())

        return (
            chat_completion.usage.total_tokens,
            first_choice(chat_completion=chat_completion),
        )

    return chat_prompt
