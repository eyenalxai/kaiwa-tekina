from aiohttp.web_request import Request
from aiohttp.web_response import Response


async def health_check_endpoint(_request: Request) -> Response:
    return Response()
