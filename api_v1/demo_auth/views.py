from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

router = APIRouter(tags=["Demo Auth"])

security = HTTPBasic()

bd_users = {
    "admin": "admin",
    "mat": "mat",
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
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


@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi, {auth_username}",
    }

