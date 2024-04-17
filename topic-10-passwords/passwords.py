import hashlib
import string
import random

def hash_password(password):
    salt = "".join(random.choices(string.hexdigits, k=32))
    password_salt = password+salt.encode("utf-8")
    hash_object = hashlib.sha256(password_salt)
    hashed_password = hash_object.hexdigest()
    return hashed_password, salt

def check_password(password, saved_hash_password, salt):
    password_salt = password.encode("utf-8") + salt
    hash_object = hashlib.sha256(password_salt)
    hashed_password = hash_object.hexdigest()
    return hashed_password == saved_hash_password

def test_hash_password():
    hashed_password, salt = hash_password("hohoho")
    assert type(hashed_password) is str
    assert type(salt) is str
    assert check_password("hoho", hashed_password, salt) == False
    assert check_password("hohoho", hashed_password, salt) == True

if __name__ == "__main__":
    test_hash_password()