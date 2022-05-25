import uuid


def generate_username() -> str:
    return f'user-{uuid.uuid4()}'
