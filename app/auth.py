from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.config import cau_hinh
from app.deps import lay_db
from app.models import User

KHOA_BI_MAT = cau_hinh.khoa_bi_mat
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/dang-nhap")


def bam_mat_khau(mat_khau: str) -> str:
    return bcrypt.hashpw(mat_khau.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def kiem_tra_mat_khau(mat_khau: str, mat_khau_bam: str) -> bool:
    return bcrypt.checkpw(mat_khau.encode("utf-8"), mat_khau_bam.encode("utf-8"))


def tao_token_truy_cap(username: str, expires_delta: int | None = None) -> str:
    het_han = datetime.now(timezone.utc) + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        {"sub": username, "exp": het_han}, KHOA_BI_MAT, algorithm=ALGORITHM
    )

def lay_user_hien_tai(token: str = Depends(oauth2_scheme), db: Session = Depends(lay_db)) -> User:
    loi_xac_thuc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token khong hop le hoac da het han",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        du_lieu = jwt.decode(
            token, cau_hinh.khoa_bi_mat, algorithms=[ALGORITHM]
        )
    except jwt.PyJWTError:
        raise loi_xac_thuc
    user = (
        db.query(User)
        .filter(User.username == du_lieu.get("sub"))
        .first()
    )
    if user is None:
        raise loi_xac_thuc
    return user

def chi_quan_tri_vien(
    user: User = Depends(lay_user_hien_tai),
) -> User:
    if not user.la_quan_tri_vien:
        raise HTTPException(status_code=403, detail="Chi quan tri vien duoc thao tac")
    return user
