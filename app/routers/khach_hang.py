from fastapi import APIRouter, Depends, Path, Query, Response
from sqlalchemy.orm import Session

from app import crud
from app.deps import lay_db
from app.schemas import KhachHangChiTiet, KhachHangRa, SuaKhachHang, TaoKhachHang

router = APIRouter(prefix="/khach-hang", tags=["KhachHang"])


@router.get("", response_model=list[KhachHangRa])
async def lay_danh_sach_khach_hang(
    tim: str | None = Query(default=None, max_length=50),
    bo_qua: int = Query(default=0, ge=0),
    gioi_han: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(lay_db),
):
    return crud.liet_ke_khach_hang(db, tim, bo_qua, gioi_han)


@router.get("/{khach_hang_id}", response_model=KhachHangChiTiet)
async def lay_mot_khach_hang(khach_hang_id: int = Path(gt=0), db: Session = Depends(lay_db)):
    return crud.lay_khach_hang_kem_don_hang(db, khach_hang_id)


@router.post("", response_model=KhachHangRa, status_code=201)
async def them_khach_hang(du_lieu: TaoKhachHang, db: Session = Depends(lay_db)):
    return crud.tao_khach_hang(db, du_lieu)


@router.put("/{khach_hang_id}", response_model=KhachHangRa)
async def sua_khach_hang(
    du_lieu: SuaKhachHang, khach_hang_id: int = Path(gt=0), db: Session = Depends(lay_db)
):
    return crud.sua_khach_hang(db, khach_hang_id, du_lieu)


@router.delete("/{khach_hang_id}", status_code=204)
async def xoa_khach_hang(khach_hang_id: int = Path(gt=0), db: Session = Depends(lay_db)):
    crud.xoa_khach_hang(db, khach_hang_id)
    return Response(status_code=204)
