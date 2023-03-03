from app.model.schema.user import User


def parse_telegram_id(message_text: str) -> int:
    parts = message_text.split()

    if len(parts) != 2:
        raise ValueError("Invalid message text provided")

    return int(parts[1])


def username_or_full_name(user: User) -> str:
    if user.username:
        return "@{username}".format(username=user.username)

    if user.full_name:
        return "{full_name}".format(full_name=user.full_name)

    return str(user.telegram_id)
