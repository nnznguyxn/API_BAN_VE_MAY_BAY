from app.database import Base, engine, SessionLocal 
from app.models import DanhSach

DU_LiEU_MAU = [
    ("KH001", "Nguyen Van A", "0123456789", "a@gmai.com"),
    ("KH002", "Tran Thi B", "0987654321", "b@gmail.com"),
    ("KH003", "Le Van C", "0193840938", "c@gmail.com"),
]

def khoi_tao_du_lieu(): 
    Base.metadata.create_all(engine)
    db=SessionLocal() 

    try: 
        if db.query(DanhSach).count()==0: 
            db.add_all(
                DanhSach(id_khach_hang=idkhachhang, ho_ten=ten, so_dien_thoai=sdt, email=email) 
                for idkhachhang, ten, sdt, email in DU_LiEU_MAU
            )
            db.commit()
    finally: 
        db.close()