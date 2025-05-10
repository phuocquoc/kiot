# 🚀 KiotViet Clone Project

Clone lại hệ thống quản lý bán hàng như KiotViet, gồm:
- Quản lý Sản phẩm
- Bán hàng (POS)
- Quản lý Kho
- Khách hàng
- Hóa đơn + In PDF
- Đổi giao diện màu người dùng
- Đăng nhập bằng JWT
- Frontend: VueJS + Tailwind
- Backend: Django REST Framework

---

## 📦 Cấu trúc thư mục
backend/ # Django project frontend/ # VueJS project db.sqlite3 # Database mẫu README.md # Hướng dẫn setup


---

## 🔥 Cách cài đặt nhanh

### 1. Chạy Backend Django
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows dùng venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
