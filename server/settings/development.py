from server.settings.base import *

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    ".herokuapp.com",
    "develop.squad06.com",
]

# In development, we don't need a secure password hasher. We can use
# MD5 instead, this is because we don't need to worry about security
# in development. However, we should use a secure password hasher in
# production, like PBKDF2 or Argon2.

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
