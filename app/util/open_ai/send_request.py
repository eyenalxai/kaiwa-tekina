from httpx import HTTPStatusError, Response

from app.config.http_client import http_client
from app.config.log import logger
from app.model.schema.open_ai import ChatGPTMessage


def send_openai_request(
    url: str,
    headers: dict[str, str],
    configuration: dict[str, str | int],
    messages: list[ChatGPTMessage],
) -> Response:
    response = http_client.post(
        url=url,
        headers=headers,
        json={
            **configuration,
            "messages": [message.dict(exclude_none=True) for message in messages],
        },
    )

    try:
        response.raise_for_status()
    except HTTPStatusError as http_status_error:
        logger.error(
            "OpenAI API error: {http_status_error}\n{response}\n{text}".format(
                http_status_error=http_status_error,
                response=(
                    http_status_error.response
                    if http_status_error.response
                    else "No response"
                ),
                text=(
                    http_status_error.response.text
                    if http_status_error.response
                    else "No response text"
                ),
            ),
        )

        raise
    except Exception as exception:
        logger.error(
            "Error: {exception}".format(exception=exception),
        )
        raise

    return response
