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
)

router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
)


@router.post("/login/", response_model=Token)
def auth_user_jwt(user: UserAuthSchema = Depends(validate_auth_user)):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type="Bearer",
    )


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
