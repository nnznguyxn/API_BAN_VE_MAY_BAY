from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

CHUOI_KET_NOI = "sqlite:///./quan_ly_ve_may_bay.db"

engine=create_engine(CHUOI_KET_NOI, connect_args={"check_same_thread": False})  
SessionLocal=sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass