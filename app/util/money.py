from app.util.settings import shared_settings


def tokens_to_usd(tokens: int) -> float:
    return round(tokens * shared_settings.per_token_price / 1000, 4)
