from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.user import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(data: RegisterRequest):
    success = register_user(data.username, data.password)

    if not success:
        raise HTTPException(status_code=400, detail="Username đã tồn tại")

    return {"message": "Đăng ký thành công"}


@router.post("/login")
def login(data: LoginRequest):
    user = login_user(data.username, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu")

    # user = (id, username)
    return {
        "id": user[0],
        "username": user[1]
    }
