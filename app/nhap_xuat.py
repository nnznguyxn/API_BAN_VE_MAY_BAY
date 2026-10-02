import csv
import io
import json
from datetime import date, datetime

COT_DON_HANG = [
    "id_khach_hang",
    "id_nhan_vien",
    "ho_ten",
    "email",
    "so_dien_thoai",
    "tong_tien",
    "ma_giam_gia",
    "trang_thai",
    "ngay_tao",
    "han_thanh_toan",
]


def doc_don_hang_tu_csv(noi_dung: str) -> list[dict]:
    cac_dong = []
    doc = csv.DictReader(io.StringIO(noi_dung))
    thieu = {"ho_ten", "email", "so_dien_thoai"} - set(doc.fieldnames or [])
    if thieu:
        raise ValueError(f"File CSV thieu cot: {', '.join(sorted(thieu))}")

    for so_thu_tu, dong in enumerate(doc, start=2):
        ho_ten = (dong.get("ho_ten") or "").strip()
        email = (dong.get("email") or "").strip()
        so_dien_thoai = (dong.get("so_dien_thoai") or "").strip()
        if not (ho_ten and email and so_dien_thoai):
            continue
        try:
            id_khach_hang = int(dong["id_khach_hang"]) if dong.get("id_khach_hang") else None
            id_nhan_vien = int(dong["id_nhan_vien"]) if dong.get("id_nhan_vien") else None
            tong_tien = float(dong["tong_tien"]) if dong.get("tong_tien") else 0.0
        except ValueError:
            raise ValueError(f"Dong {so_thu_tu}: id_khach_hang, id_nhan_vien hoac tong_tien khong phai so")

        cac_dong.append(
            {
                "id_khach_hang": id_khach_hang,
                "id_nhan_vien": id_nhan_vien,
                "ho_ten": ho_ten,
                "email": email,
                "so_dien_thoai": so_dien_thoai,
                "tong_tien": tong_tien,
                "ma_giam_gia": (dong.get("ma_giam_gia") or "").strip() or None,
                "trang_thai": (dong.get("trang_thai") or "cho thanh toan").strip(),
                "ngay_tao": dong.get("ngay_tao") or None,
                "han_thanh_toan": dong.get("han_thanh_toan") or None,
            }
        )
    return cac_dong


def ghi_don_hang_ra_csv(cac_don_hang) -> str:
    bo_dem = io.StringIO()
    ghi = csv.DictWriter(bo_dem, fieldnames=COT_DON_HANG)
    ghi.writeheader()
    for don_hang in cac_don_hang:
        ghi.writerow({cot: getattr(don_hang, cot) for cot in COT_DON_HANG if hasattr(don_hang, cot)})
    return bo_dem.getvalue()


def _doi_kieu(gia_tri):
    if isinstance(gia_tri, (date, datetime)):
        return gia_tri.isoformat()
    raise TypeError(f"Khong doi duoc kieu {type(gia_tri).__name__}")


def ghi_bao_cao_json(bao_cao: dict) -> str:
    return json.dumps(bao_cao, ensure_ascii=False, indent=2, default=_doi_kieu)


def luu_ra_file(duong_dan: str, noi_dung: str) -> int:
    with open(duong_dan, "w", encoding="utf-8") as f:
        return f.write(noi_dung)


# alias de giu tuong thich voi code cu
COT_VE = COT_DON_HANG

def doc_sach_tu_csv(noi_dung: str) -> list[dict]:
    return doc_don_hang_tu_csv(noi_dung)


def ghi_sach_ra_csv(cac_sach) -> str:
    return ghi_don_hang_ra_csv(cac_sach)
