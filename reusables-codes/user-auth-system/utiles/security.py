from pwdlib import PasswordHash

hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """ Hash a plaintext password using bcrypt """
    return hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verify a plaintext password against a hashed password """
    return hasher.verify(plain_password, hashed_password)