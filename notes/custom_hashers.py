# notes/custom_hashers.py

from django.contrib.auth.hashers import BasePasswordHasher
import hashlib

class MD5PasswordHasher(BasePasswordHasher):
    algorithm = "md5"  # Custom name for the algorithm

    def salt(self):
        # Salt is a random string that makes the hash harder to reverse.
        return str(hashlib.md5().hexdigest())  # Generate a random salt.

    def encode(self, password, salt):
        # Hash the password using MD5 and the salt
        return hashlib.md5(f"{password}{salt}".encode('utf-8')).hexdigest()

    def verify(self, password, encoded):
        # Verify the password by re-hashing it with the stored salt
        salt = encoded[:32]  # The first 32 characters of the encoded password
        return self.encode(password, salt) == encoded

    def iterations(self):
        return 1  # MD5 is fast, so no iterations like in PBKDF2
