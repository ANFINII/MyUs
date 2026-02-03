from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from config.settings.base import ENCRYPT_IV, ENCRYPT_KEY


KEY = str(ENCRYPT_KEY).encode('utf-8')
IV = str(ENCRYPT_IV).encode('utf-8')


def encrypt(data: str) -> str:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return b64encode(encrypted).decode('utf-8')


def decrypt(encrypted_base64: str) -> str:
    encrypted_data = b64decode(encrypted_base64)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = cipher.decrypt(encrypted_data)
    return unpad(decrypted, AES.block_size).decode('utf-8')
