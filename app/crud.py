from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.config import cau_hinh
from app.models import DonHang, DanhSach
from app.schemas import TaoDonHang, SuaKhachHang, TaoKhachHang

def lay_khach_hang(db:Session, id_khach_hang:int) -> DanhSach:
    khach_hang = db.get(DanhSach, id_khach_hang)
    if khach_hang is None:
        raise HTTPException(status_code=404, detail="Khong tim thay khach hang")
    return khach_hang


def lay_khach_hang_kem_don_hang(db: Session, id_khach_hang: int) -> DanhSach:
    khach_hang= ( 
        db.query(DanhSach)
        .options(selectinload(DanhSach.don_hang))
        .filter(DanhSach.id_khach_hang==id_khach_hang)
        .first()
    )
    if khach_hang is None:
        raise HTTPException(status_code=404, detail="Khong tim thay khach hang")
    return khach_hang


def liet_ke_don_hang(db: Session, tim: str | None = None, bo_qua: int = 0, gioi_han: int = 10):
    truy_van = db.query(DanhSach)
    if tim:
        truy_van = truy_van.filter(DanhSach.ten_don_hang.ilike(f"%{tim}%"))
    return truy_van.order_by(DanhSach.id_khach_hang).offset(bo_qua).limit(gioi_han).all()


def tao_khach_hang(db: Session, dulieu: TaoKhachHang) -> DanhSach:
    khach_hang=DanhSach(**dulieu.model_dump())
    db.add(khach_hang)
    try: 
        db.commit() 
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Khach hang da ton tai")
    db.refresh(khach_hang)
    return khach_hang 


def sua_khach_hang(db: Session, id_khach_hang: int, dulieu: SuaKhachHang) -> DanhSach:
    khach_hang = lay_khach_hang(db, id_khach_hang)
    for ten_cot, gia_tri in dulieu.model_dump(exclude_unset=True).items():
        setattr(khach_hang, ten_cot, gia_tri)
    db.commit()
    db.refresh(khach_hang)
    return khach_hang


def xoa_khach_hang(db: Session, id_khach_hang: int) -> None:
    db.delete(lay_khach_hang(db, id_khach_hang))
    db.commit()


def them_don_hang(db: Session, dulieu: TaoDonHang) -> DonHang:
    lay_khach_hang(db, dulieu.id_khach_hang) 
    don_hang = DonHang(**dulieu.model_dump())
    db.add(don_hang)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Don hang da ton tai")
    db.refresh(don_hang)
    return don_hang