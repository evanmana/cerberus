'''import hashlib, binascii, os


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    print(salt)

    pwdhash = hashlib.pbkdf2_hmac('sha256',
                                  password.encode('utf-8'),
                                  salt,
                                  100000,
                                  16)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha256',
                                  provided_password.encode('utf-8'),
                                  salt.encode('utf-8'),
                                  100000,
                                  16)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


a = hash_password('iraklis')

print(a)
print(verify_password(a, 'iraklis'))'''
