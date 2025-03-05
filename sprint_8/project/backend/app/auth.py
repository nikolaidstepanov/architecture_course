import time
import os

import jwt
from jwt import PyJWKClient
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer

REQUIRED_ROLE = "prothetic_user"
KEYCLOAK_URL = os.getenv("FASTAPI_APP_KEYCLOAK_URL", "http://keycloak:8080")
REALM = os.getenv("FASTAPI_APP_KEYCLOAK_REALM", "reports-realm")
JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"


jwk_client = PyJWKClient(JWKS_URL)
security = HTTPBearer()


def fetch_jwks_with_retry(retries=3, delay=2):
    for attempt in range(retries):
        try:
            return jwk_client.get_signing_keys()
        except jwt.exceptions.PyJWKClientConnectionError as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e


def verify_token(token: str):
    """
    Проверяет подпись токена через JWKS Keycloak, а также роль пользователя.
    """
    try:
        signing_keys = fetch_jwks_with_retry()
        signing_key = signing_keys[0].key
        payload = jwt.decode(token, signing_key, algorithms=["RS256"])

        roles = payload.get("realm_access", {}).get("roles", [])
        if REQUIRED_ROLE not in roles:
            raise HTTPException(status_code=403, detail="User lacks required role")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(token: str = Security(security)):
    """
    FastAPI dependency: получает и проверяет текущего пользователя.
    """
    return verify_token(token.credentials)
