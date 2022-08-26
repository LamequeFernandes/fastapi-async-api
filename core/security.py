from passlib.context import CryptContext


CRIPTO = CryptContext(schemas=['bcrypt'], deprecated='auto')


def checked_password(password: str, hash_password: str) -> bool:
    return CRIPTO.verify(password, hash_password)


def generate_hash_password(password: str) -> str:
    return CRIPTO.hash(password)
