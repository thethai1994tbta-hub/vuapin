# Vua Pin - Battery E-commerce System

Giải pháp pin lithium tối ưu cho mọi nhu cầu. Hệ thống thương mại điện tử chuyên nghiệp.

## Tính năng chính

✅ **Máy tính cấu hình pin** - Tính toán cấu hình pin (S/P) dựa trên điện áp và dung lượng  
✅ **Tính giá sản phẩm** - Tính chi phí vật liệu, giá bán đề xuất, lợi nhuận  
✅ **Quản lý sản phẩm** - Thêm, sửa, xóa sản phẩm với hình ảnh  
✅ **Tìm kiếm sản phẩm** - Tìm kiếm theo tên, mô tả, cấu hình  
✅ **Đặt hàng online** - Form đặt hàng với xác nhận email tự động  
✅ **Quản lý đơn hàng** - Dashboard quản lý đơn hàng, thống kê doanh thu  
✅ **Chính sách bảo hành** - 24 tháng bảo hành cho pin, 36 tháng cho BMS

## Yêu cầu hệ thống

- Python 3.8+
- SQLite3
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Cài đặt

### 1. Clone/Download dự án
```bash
cd /path/to/vua-pin
```

### 2. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng
```bash
python server.py
```

Truy cập: http://127.0.0.1:5000

## Sử dụng

### Trang chủ (http://127.0.0.1:5000)
- Xem sản phẩm chính
- Tìm kiếm sản phẩm
- Xem bài viết về pin lithium
- Đặt hàng trực tuyến
- Tính cấu hình pin

### Admin Dashboard (http://127.0.0.1:5000/admin)
- Quản lý sản phẩm (thêm/sửa/xóa)
- Quản lý đơn hàng
- Xem thống kê (tổng đơn, doanh thu)
- Tính giá sản phẩm

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/calculate` | Tính cấu hình pin |
| POST | `/api/calculate-price` | Tính giá sản phẩm |
| POST | `/api/order` | Tạo đơn hàng mới |
| GET | `/api/admin/orders` | Lấy tất cả đơn hàng |
| PUT | `/api/admin/order/<id>` | Cập nhật đơn hàng |
| DELETE | `/api/admin/order/<id>` | Xóa đơn hàng |
| GET | `/api/admin/products` | Lấy tất cả sản phẩm |
| POST | `/api/admin/product` | Tạo sản phẩm mới |
| PUT | `/api/admin/product/<id>` | Cập nhật sản phẩm |
| DELETE | `/api/admin/product/<id>` | Xóa sản phẩm |

## Cấu hình Email (tuỳ chọn)

Để bật xác nhận email tự động, đặt biến môi trường:

```bash
export EMAIL_SENDER="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
```

**Gmail App Password:**
1. Bật 2-factor authentication
2. Vào https://myaccount.google.com/apppasswords
3. Chọn "Mail" và "Windows Computer" (hoặc tương đương)
4. Sao chép mật khẩu ứng dụng

## Cơ sở dữ liệu

SQLite database tự động tạo tại `vuapin.db` với 3 bảng:

- **orders** - Lưu đơn hàng của khách
- **products** - Lưu danh sách sản phẩm
- **admin_users** - Dành cho authentication tương lai

## Triển khai Production

### Với Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

### Với Docker
```bash
docker build -t vua-pin .
docker run -p 5000:5000 vua-pin
```

### Với Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
```

## Bảo mật

- ✓ XSS protection: HTML escaping cho user data
- ✓ CORS enabled: Cho phép requests từ client
- ✓ Database prepared statements: SQL injection protection
- ✓ Input validation: Kiểm tra tất cả inputs

## Lỗi thường gặp

### "Database is locked"
→ Đóng tất cả instance cũ, xóa `vuapin.db`, chạy lại

### Email không gửi được
→ Kiểm tra biến môi trường, dùng Gmail App Password (không phải mật khẩu thường)

### Port 5000 đã dùng
→ Chạy: `python -c "import server; server.app.run(port=8000)"`

## Hỗ trợ

📞 Hotline: 0814830562  
💬 Zalo: 0814830562  
📧 Email: vuapin.shop@gmail.com

## License

Private - Proprietary Software
