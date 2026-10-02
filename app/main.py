from fastapi import FastAPI

from app.seed import khoi_tao_du_lieu
from app.routers import don_hang, khach_hang, auth

app=FastAPI(title="API quản lý đơn hàng vé máy bay và khách hàng")

khoi_tao_du_lieu()

app.include_router(don_hang.router)
app.include_router(khach_hang.router)
app.include_router(auth.router)

@app.get("/ping", tags=["He Thong"])
async def ping():
    return {"status": "ok"}