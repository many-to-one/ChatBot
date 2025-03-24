import secrets

def generate_secret_key():
    return secrets.token_urlsafe(32)

secret_key = generate_secret_key()
print(f"Your secret key is: {secret_key}")
