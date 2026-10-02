from pydantic import BaseModel, Field, EmailStr, ConfigDict

class TaoKhachHang(BaseModel):
    id_khach_hang:int
    ho_ten:str=Field(min_length=2, max_length=60)
    so_dien_thoai:str=Field(min_length=10, max_length=15)
    email:EmailStr

class SuaKhachHang(BaseModel):
    ho_ten:str|None=Field(default=None, min_length=2, max_length=60)
    email:EmailStr|None=None
    so_dien_thoai:str|None=Field(default=None, min_length=10, max_length=15)

class TaoDonHang(BaseModel):
    id: int
    id_khach_hang: int
    ho_ten: str
    so_dien_thoai: str
    email: EmailStr

class DonHangRa(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    id: int
    id_khach_hang: int
    ho_ten: str
    so_dien_thoai: str
    email: EmailStr
    tong_tien: float
    ma_giam_gia: str|None=None
    trang_thai: str
    ngay_tao: str
    han_thanh_toan: str|None=None

class KhachHangRa(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    id_khach_hang:int
    ho_ten:str
    so_dien_thoai:str
    email:EmailStr

class KhachHangChiTiet(KhachHangRa):
    don_hang: list[DonHangRa]=[]

class TaoUser(BaseModel):
    username:str=Field(min_length=3, max_length=50)
    password:str=Field(min_length=6, max_length=100)

class UserRa(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    id:int
    username:str

class Token(BaseModel):
    access_token:str
    token_type:str="bearer"