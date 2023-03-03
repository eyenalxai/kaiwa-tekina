def parse_telegram_id(message_text: str) -> int:
    parts = message_text.split()

    if len(parts) != 2:
        raise ValueError("Invalid message text provided")

    return int(parts[1])
