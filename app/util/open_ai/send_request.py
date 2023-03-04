from httpx import HTTPStatusError, Response

from app.config.http_client import http_client
from app.config.log import logger
from app.model.schema.open_ai import ChatGPTMessage


def send_openai_request(
    url: str,
    headers: dict[str, str],
    messages: list[ChatGPTMessage],
) -> tuple[Response, bool]:
    response = http_client.post(
        url=url,
        headers=headers,
        json={
            "model": "gpt-3.5-turbo",
            "messages": [message.dict(exclude_none=True) for message in messages],
        },
    )

    try:
        response.raise_for_status()
    except HTTPStatusError as http_status_error:
        logger.error(
            "OpenAI API error: {http_status_error}\n{response}\n{text}".format(
                http_status_error=http_status_error,
                response=http_status_error.response,
                text=(
                    http_status_error.response.text
                    if http_status_error.response.text
                    else "No response text"
                ),
            ),
        )
        return http_status_error.response, True

    except Exception as exception:
        logger.error(
            "Error: {exception}".format(exception=exception),
        )
        raise

    return response, False
