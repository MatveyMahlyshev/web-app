from fastapi import HTTPException, Depends, status, Header
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated

security = HTTPBasic()

bd_users = {
    "admin": "admin",
    "mat": "mat",
}

auth_token_to_username = {
    "070b2c340ab59b5acbd66a02665ec": "admin",
    "83ca796283326cb7b92ddba915aa9c6b582": "mat",
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    if credentials.username not in bd_users:
        raise unauthed_exc
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        bd_users[credentials.username].encode("utf-8"),
    ):
        raise unauthed_exc
    return credentials.username


def get_username_by_static_auth_token(
    auth_token: str = Header(alias="x-auth-token"),
) -> str:

    if token := auth_token_to_username.get(auth_token):
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )
