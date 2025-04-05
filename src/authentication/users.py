from fastapi import APIRouter, HTTPException, Form, Depends
from jwt import InvalidTokenError
from pydantic import EmailStr
from sqlalchemy import select
import jwt
from src.authentication.hash_password import bcrypt, verify
from src.database import SessionDepend
from src.models.tokens import Token
from src.models.users import UserModel
from src.schemas.users import UserSchema, LoginSchema
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, timezone, datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.properties import SECRET_KEY

router = APIRouter(tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
http_bearer = HTTPBearer()
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict,
                        expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@router.post("/users/register/", summary="Registers a new user.")
async def register_user(data: UserSchema,
                        new_session: SessionDepend):
    query = select(UserModel).where(UserModel.email == data.email)
    user_result = await new_session.execute(query)
    user = user_result.scalar_one_or_none()

    if user:
        raise HTTPException(status_code=401, detail="A user with this e-mail address is already registered.")

    new_user = UserModel(
        first_name=data.first_name,
        last_name=data.last_name,
        birth_date=data.birth_date,
        email=data.email,
        password=bcrypt(data.password)
    )

    new_session.add(new_user)
    await new_session.commit()
    return {"ok": "registered"}


async def get_user(new_session: SessionDepend,
                   email: EmailStr):
    query = select(UserModel).where(UserModel.email == email)
    user_result = await new_session.execute(query)
    user = user_result.scalar_one_or_none()

    return user


async def authenticate_user(new_session: SessionDepend,
                            email: EmailStr,
                            password: str):
    user = await get_user(new_session, email)

    if not user:
        return False

    if not verify(password, user.password):
        return False

    return True


@router.post("/users/login/", summary="Logs in a user.")
async def login_user(new_session: SessionDepend,
                     data: LoginSchema):
    user = await authenticate_user(new_session, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="An error has occurred. Check the data you have entered.")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": data.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(new_session: SessionDepend,
                           token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    credentials_exception = HTTPException(status_code=401,
                                          detail="An error has occurred. Could not validate credentials.")
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(new_session, email=email)
    if user is None:
        raise credentials_exception
    return user


@router.get("/users/me/", summary="Gets an information about user.")
def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "birth_date": current_user.birth_date
    }
