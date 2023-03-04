from collections.abc import Callable

from tiktoken import Encoding

from app.model.schema.open_ai import ChatCompletion, ChatGPTMessage, OpenAIError
from app.util.open_ai.send_request import send_openai_request
from app.util.settings import shared_settings


def first_choice(chat_completion: ChatCompletion) -> ChatGPTMessage:
    return min(chat_completion.choices, key=lambda choice: choice.index).message


def token_reducer(
    previous_messages: list[ChatGPTMessage],
    tokenizer: Encoding,
) -> list[ChatGPTMessage]:
    total_tokens = sum(
        len(tokenizer.encode(message.content)) for message in previous_messages
    )

    while total_tokens > shared_settings.max_tokens_per_request:
        previous_messages.pop(0)
        total_tokens = sum(
            len(tokenizer.encode(message.content)) for message in previous_messages
        )

    return previous_messages


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
