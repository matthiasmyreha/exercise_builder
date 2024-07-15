import secrets
import string


def generate_random(length=6):
    characters = string.ascii_letters + string.digits
    random_hash = "".join(secrets.choice(characters) for _ in range(length))
    return random_hash
