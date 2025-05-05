from fastapi import (
    HTTPException,
    Depends,
    status,
    Header,
    Response,
    Cookie,
    Form,
)
from datetime import timedelta
from jwt.exceptions import InvalidTokenError
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from typing import (
    Annotated,
    Any,
)
import secrets
import uuid

from users.schemas import UserAuthSchema
from auth import utils as auth_utils
from core.config import settings


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt/login/",
)
http_bearer = HTTPBearer(auto_error=False)

security = HTTPBasic()

bd_users = {
    "admin": "admin",
    "mat": "mat",
}

auth_token_to_username = {
    "070b2c340ab59b5acbd66a02665ec": "admin",
    "83ca796283326cb7b92ddba915aa9c6b582": "mat",
}

COOKIES: dict[str, dict[str, Any]] = {}
COOKIES_SESSION_ID_KEY = "web-app-session-id"

john = UserAuthSchema(
    username="John",
    password=auth_utils.hash_password("QwertyUiop44"),
    email="john@asdsad.ru",
)

matthew = UserAuthSchema(
    username="Matthew",
    password=auth_utils.hash_password("Adepaz17_"),
    email="matthew@asdsad.ru",
)


users_db: dict[str, UserAuthSchema] = {}

users_db[john.username] = john
users_db[matthew.username] = matthew


def generate_session_id() -> str:
    return uuid.uuid4().hex


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


def get_session_data(
    session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY),
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    return COOKIES[session_id]


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not correct username or password",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exception

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exception
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return user


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> UserAuthSchema:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Error type of token.",
    )


def get_user_by_token_sub(payload: dict) -> UserAuthSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserAuthSchema:
    validate_token_type(
        payload=payload,
        token_type=ACCESS_TOKEN_TYPE,
    )
    return get_user_by_token_sub(payload=payload)


def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
) -> UserAuthSchema:
    validate_token_type(payload=payload, token_type=REFRESH_TOKEN_TYPE)
    return get_user_by_token_sub(payload=payload)


def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserAuthSchema:
        validate_token_type(
            payload=payload,
            token_type=token_type,
        )
        return get_user_by_token_sub(payload=payload)
    return get_auth_user_from_token

get_current_auth_user = get_auth_user_from_token_of_type(token_type=ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(token_type=REFRESH_TOKEN_TYPE)



def get_current_active_auth_user(user: UserAuthSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not active user",
    )





def create_token(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserAuthSchema) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_token(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: UserAuthSchema) -> str:
    jwt_payload = {
        "sub": user.username,
    }
    return create_token(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
