import random
from datetime import datetime, timedelta

# Giá khởi điểm
gia_hien_tai = 35000

# Ngày bắt đầu (1 tháng 1 năm 2015)
ngay = datetime(2015, 1, 1)

# Ngày kết thúc (31 tháng 12 năm 2024)
ngay_ket_thuc = datetime(2024, 12, 31)

# Mở file để ghi
with open("gia_ca.csv", "w", encoding="utf-8") as f:
    while ngay <= ngay_ket_thuc:
        thang = ngay.month

        # Xác định xu hướng theo tháng
        if 1 <= thang <= 4:
            # Xu hướng tăng: biên độ dao động lệch về dương
            thay_doi = random.randint(-5, 10)
        elif 5 <= thang <= 10:
            # Xu hướng giảm: biên độ dao động lệch về âm
            thay_doi = random.randint(-10, 5)
        else:
            # Tháng 11-12: xu hướng tăng lại
            thay_doi = random.randint(-5, 10)

        # Cập nhật giá
        gia_hien_tai = gia_hien_tai + thay_doi * 100

        # Đảm bảo giá không âm và không thấp hơn 10.000 đồng
        gia = max(gia_hien_tai, 10000)

        # Ghi ra file: định dạng YYYY-MM-DD: giá
        f.write(f"{ngay.strftime('%Y-%m-%d')}: {gia}\n")

        # Tăng ngày
        ngay += timedelta(days=1)

print("gia_ca.csv")
