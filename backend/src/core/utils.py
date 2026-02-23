import string
from random import choice
from src.core.config import settings


ALPHABET = string.ascii_letters + string.digits

def generate_random_code(length: int = settings.CODE_LENGTH) -> str:
    code = ""
    for _ in range(length):
        code += choice(ALPHABET)
    return code

def make_short_url(code:str) -> str:
    return f"{settings.APP_HOST}/{code}"
