def tokens_to_usd(*, tokens: int, per_token_price: float) -> float:
    return round(tokens * per_token_price / 1000, 2)
