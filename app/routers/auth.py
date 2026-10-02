from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import (
    bam_mat_khau,
    kiem_tra_mat_khau,
    tao_token_truy_cap,
)
from app.deps import lay_db
from app.models import User
from app.schemas import TaoUser, Token, UserRa

router = APIRouter(prefix="/auth", tags=["Xac thuc"])


@router.post("/dang-ky", response_model=UserRa, status_code=201)
async def dang_ky(du_lieu: TaoUser, db: Session = Depends(lay_db)):
    nguoi_dung = User(
        username=du_lieu.username,
        password=bam_mat_khau(du_lieu.password),
    )
    db.add(nguoi_dung)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ten nguoi dung da ton tai")
    db.refresh(nguoi_dung)
    return nguoi_dung


@router.post("/dang-nhap", response_model=Token)
async def dang_nhap(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(lay_db),
):
    user = (
        db.query(User).filter(User.username == form_data.username).first()
    )
    if user is None or not kiem_tra_mat_khau(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Sai ten nguoi dung hoac mat khau"
        )

    return Token(access_token=tao_token_truy_cap(user.username))