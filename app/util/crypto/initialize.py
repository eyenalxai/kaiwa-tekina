from cryptography.fernet import Fernet


def initialize_fernet(key: bytes) -> Fernet:
    return Fernet(key)
