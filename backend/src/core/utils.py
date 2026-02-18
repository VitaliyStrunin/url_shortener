import string
from random import choice
from src.core.config import CODE_LENGTH


ALPHABET = string.ascii_letters + string.digits

def generate_random_code(length: int = CODE_LENGTH) -> str:
    code = ""
    for _ in range(length):
        code += choice(ALPHABET)
    return code