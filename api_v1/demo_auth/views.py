from fastapi import APIRouter, Depends, Response, Cookie
from time import time
from . import auth_helpers as ah

router = APIRouter(tags=["Demo Auth"])


@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(ah.get_auth_user_username),
):
    return {
        "message": f"Hi, {auth_username}",
    }


@router.get("/http-header-auth/")
def demo_auth_header(
    username: str = Depends(ah.get_username_by_static_auth_token),
):
    return {
        "message": f"Hi, {username}",
    }


@router.post("/login-cookie/")
def demo_auth_login_set_cookie(
    response: Response,
    auth_username: str = Depends(ah.get_username_by_static_auth_token),
):
    session_id = ah.generate_session_id()
    ah.COOKIES[session_id] = {
        "username": auth_username,
        "login_at": int(time()),
    }
    response.set_cookie(
        ah.COOKIES_SESSION_ID_KEY,
        session_id,
    )
    return {
        "status": "ok",
    }


@router.get("/check-cookie/")
def demo_auth_check_cookie(user_session_data: dict = Depends(ah.get_session_data)):
    username = user_session_data["username"]
    return {
        "username": username,
        **user_session_data,
    }


@router.get("/logout-cookie/")
def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=ah.COOKIES_SESSION_ID_KEY),
    user_session_data: dict = Depends(ah.get_session_data),
):
    ah.COOKIES.pop(session_id)
    username = user_session_data["username"]
    response.delete_cookie(ah.COOKIES_SESSION_ID_KEY)
    return {
        "message": f"{username}",
    }
