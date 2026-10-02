from pydantic_settings import BaseSettings, SettingsConfigDict


class CauHinh(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ten_ung_dung: str = "API Thu Vien Quan Ly Ve May Bay"
    chuoi_ket_noi: str = "sqlite:///./thu_vien_quan_ly_ve_may_bay.db"
    khoa_bi_mat: str = "dev-secret"
    so_phut_het_han: int = 30
    nguon_cho_phep: str = "*"
    tien_phat_moi_ngay: int = 5000
    chinh_sach_phat: str = "theo_ngay"   # hoac "bac_thang"
    so_ngay_duoc_muon: int = 14
    so_sach_toi_da: int = 3
    tao_du_lieu_mau: bool = True


cau_hinh = CauHinh()
