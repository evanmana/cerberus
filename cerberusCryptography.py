import base64
import binascii
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

salt = None
password = None


def getMasterKey():
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
        backend=backend
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode())).decode()
    return key


def createNewPassword(_newPasswd):
    print("PASSWORD:\t", _newPasswd)
    backend = default_backend()
    salt = os.urandom(16)
    salt = base64.b64encode(salt).decode('utf-8')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
        backend=backend
    )
    key = base64.urlsafe_b64encode(kdf.derive(_newPasswd.encode())).decode()

    print("Salt:\t", salt)
    print("Key:\t", key)

    return salt, _newPasswd


def encrypt(_text):
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
        backend=backend
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)

    encrypted = f.encrypt(_text.encode())
    return encrypted.decode()


def decrypt(_text):
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
        backend=backend
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)

    try:
        decrypted = f.decrypt(_text.encode())
        return decrypted.decode()
    except:
        return None
