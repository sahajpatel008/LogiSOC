# auth.py
import requests
from jose import jwt
from flask import request, abort


CLERK_JWT_ISSUER = "https://infinite-pig-43.clerk.accounts.dev"
CLERK_JWKS_URL = "https://infinite-pig-43.clerk.accounts.dev/.well-known/jwks.json"
CLERK_AUDIENCE = "https://infinite-pig-43.clerk.accounts.dev"  # Example: 'clerk.website.com' or from your Clerk dashboard

# jwks = requests.get(CLERK_JWKS_URL).json()
response = requests.get(CLERK_JWKS_URL)
print("Raw JWKS response:", response.text)  # 🔍 See what's being returned
jwks = response.json()

def get_public_key(token):
    unverified_header = jwt.get_unverified_header(token)
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            return key
    raise Exception("Public key not found.")

def verify_clerk_token():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        abort(401, description="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]

    try:
        public_key = get_public_key(token)
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=CLERK_AUDIENCE,
            issuer=CLERK_JWT_ISSUER
        )
        return payload  # contains user info
    except Exception as e:
        print("Token verification failed:", e)
        abort(401, description="Token verification failed")
