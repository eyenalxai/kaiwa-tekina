from httpx import Client, Timeout

timeout = Timeout(120.0, connect=120.0, read=120.0)  # noqa: WPS432 Found magic number
http_client = Client(timeout=timeout)
