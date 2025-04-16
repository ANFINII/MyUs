from cryptography.fernet import Fernet


def create_key():
    key = Fernet.generate_key()
    return key.decode("utf-8")


def encrypt(key: str, data: str):
    fernet = Fernet(bytes(key, "utf-8"))
    encrypted = fernet.encrypt(bytes(data, "utf-8"))
    return encrypted.decode("utf-8")


def decrypt(key: str, data: str):
    fernet = Fernet(bytes(key, "utf-8"))
    decrypted = fernet.decrypt(bytes(data, "utf-8"))
    return decrypted.decode("utf-8")
