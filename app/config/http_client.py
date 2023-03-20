from httpx import Client, Timeout

timeout = Timeout(timeout=120)  # noqa: WPS432 Found magic number
http_client = Client(timeout=timeout)
