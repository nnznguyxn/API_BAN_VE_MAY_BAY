from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from sqlalchemy.orm import Session

from app.deps import lay_db
from app.models import DanhSach, TrangThaiDonHang
from app.schemas import DonHangRa, TaoDonHang

router = APIRouter(prefix="/don-hang", tags=["DonHang"])


@router.get("", response_model=list[DonHangRa])
async def liet_ke_don_hang(
    tim: str | None = Query(default=None, max_length=50),
    bo_qua: int = Query(default=0, ge=0),
    gioi_han: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(lay_db),
):
    truy_van = db.query(DanhSach)
    if tim:
        truy_van = truy_van.filter(DanhSach.ho_ten.ilike(f"%{tim}%"))
    return truy_van.order_by(DanhSach.id).offset(bo_qua).limit(gioi_han).all()


@router.get("/{don_hang_id}", response_model=DonHangRa)
async def lay_don_hang(don_hang_id: int = Path(gt=0), db: Session = Depends(lay_db)):
    don_hang = db.get(DanhSach, don_hang_id)
    if don_hang is None:
        raise HTTPException(status_code=404, detail="Khong tim thay don hang")
    return don_hang


@router.post("", response_model=DonHangRa, status_code=201)
async def tao_don_hang(du_lieu: TaoDonHang, db: Session = Depends(lay_db)):
    don_hang = DanhSach(
        id_khach_hang=du_lieu.id_khach_hang,
        ho_ten=du_lieu.ho_ten,
        email=du_lieu.email,
        so_dien_thoai=du_lieu.so_dien_thoai,
        tong_tien=0.0,
        trang_thai=TrangThaiDonHang.PENDING,
    )
    db.add(don_hang)
    db.commit()
    db.refresh(don_hang)
    return don_hang


@router.delete("/{don_hang_id}", status_code=204)
async def xoa_don_hang(don_hang_id: int = Path(gt=0), db: Session = Depends(lay_db)):
    don_hang = db.get(DanhSach, don_hang_id)
    if don_hang is None:
        raise HTTPException(status_code=404, detail="Khong tim thay don hang")
    db.delete(don_hang)
    db.commit()
    return Response(status_code=204)
