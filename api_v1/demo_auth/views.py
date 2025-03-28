from fastapi import APIRouter, Depends
from . import auth_helpers

router = APIRouter(tags=["Demo Auth"])


@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(auth_helpers.get_auth_user_username),
):
    return {
        "message": f"Hi, {auth_username}",
    }


@router.get("/http-header-auth/")
def demo_auth_header(
    username: str = Depends(auth_helpers.get_username_by_static_auth_token),
):
    return {
        "message": f"Hi, {username}",
    }
