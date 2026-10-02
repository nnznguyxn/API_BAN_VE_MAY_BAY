from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime,
    Boolean,
    ForeignKey,
    func,
    Float,
    CheckConstraint, 
    Index,
    true,
    false,
    UniqueConstraint,
    Numeric,
    Enum as SQLEnum,
    )

from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base
from enum import Enum 


class TrangThaiDonHang(str, Enum): 
    PENDING = "cho thanh toan" 
    PAID = "da thanh toan"
    CANCELED = "da huy"
    EXPIRED = "qua han giu cho" 

class NhanVien(Base):
    __tablename__ = "nhan_vien"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ho_ten: Mapped[str] = mapped_column(String(100), nullable=False)
    chuc_vu: Mapped[str | None] = mapped_column(String(50), nullable=True)

class DanhSach(Base):
    __tablename__ = "khach_hang"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_khach_hang: Mapped[int] = mapped_column(nullable=False, default=0)
    id_nhan_vien: Mapped[int | None] = mapped_column(ForeignKey("nhan_vien.id"), nullable=True)

    ho_ten: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    so_dien_thoai: Mapped[str] = mapped_column(String(15), nullable=False)

    tong_tien: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0.0)
    ma_giam_gia: Mapped[str | None] = mapped_column(String(50), nullable=True) 

    trang_thai: Mapped[TrangThaiDonHang] = mapped_column( 
        SQLEnum(TrangThaiDonHang), default=TrangThaiDonHang.PENDING, nullable=False
    )
    ngay_tao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    han_thanh_toan: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    danh_sach_khach_hang: Mapped[list["DonHang"]] = relationship(
        back_populates="don_hang",
        cascade="all, delete-orphan",
        foreign_keys="[DonHang.id_don_hang]",
    )
    
    def __repr__(self) -> str:
        return f"<DanhSach(id={self.id}, ho_ten='{self.ho_ten}', email='{self.email}', so_dien_thoai='{self.so_dien_thoai}', tong_tien={self.tong_tien}, ma_giam_gia='{self.ma_giam_gia}', trang_thai='{self.trang_thai}', ngay_tao='{self.ngay_tao}', han_thanh_toan='{self.han_thanh_toan}')>"

class DonHang(Base):
    __tablename__ = "don_hang"
    __table_args__ = ( 
        UniqueConstraint("id_don_hang", "so_cccd_passport", name="uq_don_hang_khach_hang"),
        Index("ix_khach_hang_don_ten", "id_don_hang", "ho_ten"),
        CheckConstraint("hanh_ly_ky_gui >= 0.0 AND hanh_ly_ky_gui <= 50.0", name="ck_hanh_ly_hop_le"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_don_hang: Mapped[int] = mapped_column(ForeignKey("khach_hang.id"), nullable=False)

    ho_ten: Mapped[str] = mapped_column(String(100), nullable=False)
    so_cccd_passport: Mapped[str] = mapped_column(String(20), nullable=False)
    hanh_ly_ky_gui: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    ngay_tao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    don_hang: Mapped["DanhSach"] = relationship(
        back_populates="danh_sach_khach_hang",
        foreign_keys=[id_don_hang],
    )

    def __repr__(self):
        return f"<DonHang(id={self.id}, id_don_hang={self.id_don_hang}, ho_ten='{self.ho_ten}', so_cccd_passport='{self.so_cccd_passport}', hanh_ly_ky_gui={self.hanh_ly_ky_gui}, ngay_tao='{self.ngay_tao}')>"

class User(Base):
    __tablename__ = "user" 

    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    username:Mapped[str]=mapped_column(
                                        String(50), 
                                        unique=True, 
                                        nullable=False
                                    )
    password: Mapped[str]=mapped_column(
                                        String(60), 
                                        nullable=False
                                    )
    la_admin: Mapped[bool]=mapped_column(
                                        Boolean, 
                                        default=False,
                                        server_default=false(), 
                                        nullable=False
                                    )