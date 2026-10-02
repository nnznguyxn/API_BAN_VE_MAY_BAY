from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.deps import lay_db
from app.models import DanhSach
from app.schemas import DonHangRa

router = APIRouter(prefix="/ve", tags=["VeMayBay"])


@router.get("", response_model=list[DonHangRa])
async def liet_ke_ve(
    tim: str | None = Query(default=None, max_length=50),
    bo_qua: int = Query(default=0, ge=0),
    gioi_han: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(lay_db),
):
    truy_van = db.query(DanhSach)
    if tim:
        truy_van = truy_van.filter(DanhSach.ho_ten.ilike(f"%{tim}%"))
    return truy_van.order_by(DanhSach.id).offset(bo_qua).limit(gioi_han).all()
