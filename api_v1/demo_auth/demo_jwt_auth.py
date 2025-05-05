from fastapi import (
    APIRouter,
    Depends,
    Form,
)


from users.schemas import UserAuthSchema
from auth import utils as auth_utils
from auth.schemas import Token
from .auth_helpers import (
    validate_auth_user,
    get_current_active_auth_user,
    get_current_token_payload,
    create_access_token,
    create_refresh_token,
    http_bearer,
    get_current_auth_user_for_refresh,
)

router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/login/", response_model=Token)
def auth_user_jwt(user: UserAuthSchema = Depends(validate_auth_user)):
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh/",
    response_model=Token,
    response_model_exclude_none=True,
)
def auth_refresh_jwt(user: UserAuthSchema = Depends(get_current_auth_user_for_refresh)):
    access_token = create_access_token(user=user)
    return Token(access_token=access_token)


@router.get("/users/me/")
def auth_user_check_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserAuthSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
