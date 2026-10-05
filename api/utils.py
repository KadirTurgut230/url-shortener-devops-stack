import random
import string

BASE62_ALPHABET = string.ascii_letters + string.digits

def generate_short_code(length: int = 6) -> str:
    return ''.join(random.choice(BASE62_ALPHABET) for _ in range(length))
