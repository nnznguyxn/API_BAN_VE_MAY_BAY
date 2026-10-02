from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastapi import HTTPException

from app.models import DanhSach, DonHang, TrangThaiDonHang


@dataclass
class NguCanhBanVe:
    don_hang: DanhSach
    khach_hang: DanhSach
    dang_giu: list[DonHang]
    so_ve_toi_da: int


class QuyTacDatVe(ABC):
    ly_do: str = "Khong dat dieu kien dat ve"

    @abstractmethod
    def dat(self, ngu_canh: NguCanhBanVe) -> bool:
        """True neu dieu kien dat ve duoc thoa."""

    def kiem_tra(self, ngu_canh: NguCanhBanVe) -> None:
        if not self.dat(ngu_canh):
            raise HTTPException(status_code=409, detail=self.mo_ta(ngu_canh))

    def mo_ta(self, ngu_canh: NguCanhBanVe) -> str:
        return self.ly_do

    def __repr__(self):
        return f"<{type(self).__name__}>"


class DonHangConHieuLuc(QuyTacDatVe):
    ly_do = "Don hang da bi huy hoac qua han"

    def dat(self, ngu_canh: NguCanhBanVe) -> bool:
        return ngu_canh.don_hang.trang_thai not in {
            TrangThaiDonHang.CANCELED,
            TrangThaiDonHang.EXPIRED,
        }


class ConVeTrong(QuyTacDatVe):
    ly_do = "Khong con ve phu hop de dat"

    def dat(self, ngu_canh: NguCanhBanVe) -> bool:
        return len(ngu_canh.dang_giu) < ngu_canh.so_ve_toi_da

    def mo_ta(self, ngu_canh: NguCanhBanVe) -> str:
        return f"Moi khach hang chi duoc dat toi da {ngu_canh.so_ve_toi_da} ve"


class KhongDatTrungVe(QuyTacDatVe):
    ly_do = "Khach hang da dat ve nay roi"

    def dat(self, ngu_canh: NguCanhBanVe) -> bool:
        return all(
            ve.id_don_hang != ngu_canh.don_hang.id for ve in ngu_canh.dang_giu
        )


QUY_TAC_DAT_VE: list[QuyTacDatVe] = [
    DonHangConHieuLuc(),
    ConVeTrong(),
    KhongDatTrungVe(),
]


class ChinhSachGiaVe(ABC):
    """Cach quy doi so luong ve thanh tong gia tien."""

    @abstractmethod
    def tinh(self, so_ve: int) -> float:
        """Tra ve tong tien theo phuong thuc tinh gia ve."""

    def __repr__(self):
        return f"<{type(self).__name__}>"


class GiaTheoVe(ChinhSachGiaVe):
    """Mỗi vé theo mức giá cố định."""

    def __init__(self, gia_mot_ve: float):
        self.gia_mot_ve = gia_mot_ve

    def tinh(self, so_ve: int) -> float:
        return max(0, so_ve) * self.gia_mot_ve


class GiaTheoTang(ChinhSachGiaVe):
    """Nhiều vé đầu tính theo giá thường, từ mức thứ n bắt đầu tăng giá."""

    def __init__(self, gia_mot_ve: float, nguong: int = 3):
        self.gia_mot_ve = gia_mot_ve
        self.nguong = nguong

    def tinh(self, so_ve: int) -> float:
        so_ve = max(0, so_ve)
        if so_ve <= self.nguong:
            return so_ve * self.gia_mot_ve
        vuot = so_ve - self.nguong
        return (self.nguong * self.gia_mot_ve) + (vuot * self.gia_mot_ve * 1.5)


def chon_chinh_sach_gia(ten: str, gia_mot_ve: float) -> ChinhSachGiaVe:
    """Chon chinh sach gia ve lien quan toi he thong ban ve may bay."""
    if ten == "tang_gia":
        return GiaTheoTang(gia_mot_ve)
    return GiaTheoVe(gia_mot_ve)
