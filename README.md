# TMDT_Ban_Coffee

Đồ án cuối kỳ môn Thương mại điện tử: **hệ thống thương mại điện tử bán lẻ cà phê tích hợp truy xuất và giám sát mẻ rang bằng IoT (dữ liệu mô phỏng).**

- Hướng đồ án: Hướng 1 (MVP hệ thống TMĐT), có thêm module IoT mô phỏng truy xuất mẻ rang.
- Mô hình: B2C, một cơ sở rang duy nhất (không phải marketplace).
- Luồng bắt buộc theo yêu cầu thầy: tìm kiếm, chọn sản phẩm, giỏ hàng, đặt hàng và thanh toán (mô phỏng), theo dõi trạng thái đơn.

> README này viết cho cả thành viên nhóm lẫn trợ lý AI mà các bạn dùng để hỗ trợ. Mục 9 là phần tóm tắt ngữ cảnh dành riêng cho AI.

---

## 1. Công nghệ

| Phần         | Công nghệ                                    | Ghi chú                                                             |
| ------------ | -------------------------------------------- | ------------------------------------------------------------------- |
| Backend      | Python 3.12, Django 6, Django REST Framework | Viết REST API trả JSON                                              |
| Xác thực     | Token (`rest_framework.authtoken`)           | Đăng nhập nhận token, gửi kèm header `Authorization: Token <token>` |
| CSDL         | SQLite (giai đoạn đầu)                       | Có thể chuyển sang PostgreSQL sau                                   |
| Frontend     | React + Vite + Chart.js                      | Chưa dựng, thư mục `frontend/` đang trống                           |
| Kiểm thử API | Postman hoặc Hoppscotch                      | Dùng cái nào cũng được                                              |
| Môi trường   | conda, tên môi trường `tmdt`                 |                                                                     |

**Quy tắc của môn:** KHÔNG dùng trang `/admin` có sẵn của Django. Phần quản trị do nhóm tự viết bằng API (và sau này là giao diện React). Vì vậy `django.contrib.admin` đã bị gỡ khỏi `INSTALLED_APPS`; đừng thêm lại và đừng tạo file `admin.py`.

---

## 2. Cấu trúc thư mục

```
TMDT_Ban_Coffee/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/              # Cấu hình chung: settings.py, urls.py
│   └── catalog/             # App mẫu: danh mục cà phê
│       ├── models.py        # Bảng Product
│       ├── serializers.py   # Chuyển Product <-> JSON
│       ├── views.py         # API công khai cho khách (xem, tìm, lọc)
│       ├── admin_views.py   # API quản trị (thêm, sửa, ẩn) - cần token + quyền staff
│       ├── urls.py          # Đường dẫn của app
│       └── management/commands/seed_products.py   # Nạp dữ liệu mẫu
├── frontend/                # React (chưa làm)
├── docs/                    # Tài liệu: sơ đồ CSDL, hợp đồng API, báo cáo nháp
├── .gitignore
└── README.md
```

Kiến trúc là **modular monolith**: một dự án Django duy nhất, chia thành nhiều app (mỗi app là một module nghiệp vụ). `catalog` là app mẫu, các module khác làm theo cùng khuôn.

---

## 3. Cài đặt lần đầu (mỗi người làm trên máy mình)

Yêu cầu: đã cài Git và Miniconda. Các lệnh dưới đây dùng cho Linux/macOS hoặc WSL. Trên Windows nên dùng WSL hoặc Anaconda Prompt.

```bash
# 1. Lấy code về
git clone https://github.com/hdtran112-cyber/TMDT_Ban_Coffee.git
cd TMDT_Ban_Coffee

# 2. Tạo và bật môi trường conda
conda create -n tmdt python=3.12 -y
conda activate tmdt

# 3. Cài thư viện
pip install -r backend/requirements.txt

# 4. Tạo cơ sở dữ liệu và nạp dữ liệu mẫu
cd backend
python manage.py migrate
python manage.py seed_products

# 5. Tạo tài khoản quản trị của RIÊNG BẠN (để thử API quản trị)
python manage.py createsuperuser

# 6. Chạy máy chủ
python manage.py runserver
```

Mở `http://127.0.0.1:8000/api/products/`. Thấy danh sách JSON 3 loại cà phê là cài thành công.

Lưu ý:

- File `db.sqlite3` KHÔNG được đưa lên Git. Mỗi người có cơ sở dữ liệu riêng trên máy mình, nên mỗi người phải tự chạy `migrate`, `seed_products` và `createsuperuser`.
- Mỗi lần mở terminal mới phải chạy lại `conda activate tmdt`. Đầu dòng terminal phải hiện `(tmdt)`.
- Mọi lệnh `python manage.py ...` phải chạy trong thư mục `backend/` (nơi có file `manage.py`).
- Khi mật khẩu bị Django chê yếu: dùng mật khẩu từ 8 ký tự, có cả chữ và số, hoặc gõ `y` khi được hỏi có bỏ qua kiểm tra không (chỉ dùng cho máy cá nhân khi làm thử).

---

## 4. API hiện có

Địa chỉ gốc: `http://127.0.0.1:8000/api/`

### Dành cho khách (không cần đăng nhập)

| Phương thức | Đường dẫn         | Mô tả                                                                                               |
| ----------- | ----------------- | --------------------------------------------------------------------------------------------------- |
| GET         | `/products/`      | Danh sách sản phẩm đang bán. Tham số: `q` (tìm theo tên), `roast_level` (`light`, `medium`, `dark`) |
| GET         | `/products/<id>/` | Chi tiết một sản phẩm                                                                               |

### Đăng nhập

| Phương thức | Đường dẫn      | Mô tả                                                                         |
| ----------- | -------------- | ----------------------------------------------------------------------------- |
| POST        | `/auth/login/` | Body JSON `{"username": "...", "password": "..."}`. Trả về `{"token": "..."}` |

### Dành cho quản trị (cần header `Authorization: Token <token>` và tài khoản có quyền staff)

| Phương thức | Đường dẫn               | Mô tả                                                         |
| ----------- | ----------------------- | ------------------------------------------------------------- |
| GET         | `/admin/products/`      | Danh sách mọi sản phẩm kể cả đã ẩn                            |
| POST        | `/admin/products/`      | Thêm sản phẩm. Thành công trả 201                             |
| GET         | `/admin/products/<id>/` | Chi tiết                                                      |
| PATCH / PUT | `/admin/products/<id>/` | Sửa sản phẩm                                                  |
| DELETE      | `/admin/products/<id>/` | **Ẩn** sản phẩm (`is_active = false`), không xóa hẳn. Trả 204 |

Ví dụ body thêm sản phẩm:

```json
{
  "name": "Culi Đắk Lắk",
  "price_vnd": 140000,
  "stock": 30,
  "bean_type": "Culi",
  "roast_level": "medium"
}
```

Mã trạng thái thường gặp: 200 thành công, 201 đã tạo, 204 thành công không có nội dung, 400 dữ liệu sai hoặc thiếu, 401 chưa đăng nhập, 403 không đủ quyền, 404 không tìm thấy.

Thử bằng Postman: nhớ gõ địa chỉ đầy đủ có `http://127.0.0.1:8000`, body chọn `raw` + `JSON`, và thêm header `Authorization` khi gọi API quản trị.

---

## 5. Phân công module

Mỗi người phụ trách một module (một hoặc hai Django app). Điền tên vào bảng:

| Mã  | Module                                                      | Django app dự kiến          | Phụ trách  |
| --- | ----------------------------------------------------------- | --------------------------- | ---------- |
| A   | Catalog và tìm kiếm                                         | `catalog` (đã có khuôn mẫu) | (điền tên) |
| B   | Giỏ hàng, đơn hàng, thanh toán mô phỏng                     | `orders`, `payments`        | (điền tên) |
| C   | Mẻ rang và IoT mô phỏng, trang truy xuất                    | `roasting`                  | (điền tên) |
| D   | Nền tảng: CSDL, hợp đồng API, đăng nhập, kiểm thử, tài liệu | `accounts`, `docs/`         | (điền tên) |

Quy định môn: **chép nguyên văn nội dung do AI tạo ra thì cả nhóm bị 0 điểm**. Mỗi người tự viết phần báo cáo của module mình, ý tưởng phải của nhóm, và phải giải thích được code mình nộp. AI dùng để hiểu và gỡ lỗi, không dùng để làm hộ cả phần.

---

## 6. Quy trình làm việc với Git

Không ai đẩy trực tiếp vào nhánh `main`. Mỗi người làm trên nhánh riêng.

```bash
# Đầu buổi làm việc: cập nhật main
git checkout main
git pull

# Tạo nhánh cho module của mình (đặt tên theo module)
git checkout -b feature/orders

# Làm việc, rồi lưu từng bước nhỏ
git add .
git commit -m "Them model Order va API tao don hang"

# Đẩy nhánh lên GitHub
git push -u origin feature/orders
```

Sau đó vào trang GitHub, bấm **Compare & pull request**, nhờ một bạn khác xem rồi bấm **Merge**. Gộp xong, mọi người chạy `git checkout main` rồi `git pull` để lấy bản mới.

Sau khi `git pull` lấy về thay đổi của người khác, hãy chạy thêm:

```bash
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
```

Quy tắc commit:

- Commit nhỏ, thường xuyên, thông điệp ghi rõ đã làm gì.
- Không đưa lên Git: `db.sqlite3`, `.env`, `__pycache__/`, `.venv/`, `node_modules/`, thư mục `.vscode/` (đã nằm trong `.gitignore`). Tuyệt đối không đưa mật khẩu, token hay khóa bí mật lên kho.
- Nếu thêm thư viện mới: cài xong chạy `pip freeze > backend/requirements.txt` rồi commit file đó.

Khi hai người sửa cùng một file và Git báo xung đột (conflict), đừng hoảng: mở file, tìm các dòng có `<<<<<<<`, `=======`, `>>>>>>>`, chọn nội dung đúng cần giữ rồi xóa các dòng ký hiệu, sau đó `git add` và `git commit`. Để hạn chế xung đột, mỗi người chỉ sửa trong app của mình; hai file dùng chung là `config/settings.py` và `config/urls.py`, nên sửa ít và báo trong nhóm trước.

---

## 7. Cách tạo một module mới (theo khuôn của `catalog`)

Ví dụ làm module `orders`:

```bash
cd backend
python manage.py startapp orders
```

1. Mở `config/settings.py`, thêm `'orders',` vào `INSTALLED_APPS`.
2. Viết bảng dữ liệu trong `orders/models.py` (mỗi bảng là một class kế thừa `models.Model`).
3. Tạo bảng trong CSDL:
   ```bash
   python manage.py makemigrations orders
   python manage.py migrate
   ```
4. Viết `orders/serializers.py` (dùng `ModelSerializer`), `orders/views.py` (dùng `generics.ListAPIView`, `CreateAPIView`... của DRF) và `orders/urls.py`.
5. Nối đường dẫn vào `config/urls.py`: thêm dòng `path('api/', include('orders.urls')),` vào `urlpatterns`.
6. Chức năng chỉ dành cho quản trị: đặt `permission_classes = [IsAdminUser]` (xem `catalog/admin_views.py`).
7. Chức năng cần đăng nhập nhưng không cần quyền quản trị: dùng `IsAuthenticated`.
8. Thử bằng Postman, rồi commit và tạo Pull Request.

Quy ước đặt tên đường dẫn: danh từ số nhiều, viết thường (`/orders/`, `/carts/`); chức năng quản trị đặt dưới tiền tố `/admin/`.

Quy ước thiết kế cần giữ:

- Logic nghiệp vụ (tính tiền, kiểm tra tồn kho, kiểm tra quyền) nằm ở **backend**, không để frontend quyết.
- Backend kiểm tra dữ liệu từ client: sản phẩm có tồn tại không, số lượng hợp lệ không, đủ tồn kho không.
- Không xóa hẳn dữ liệu đã được tham chiếu (đơn hàng, sản phẩm); dùng cờ như `is_active` để ẩn.

---

## 8. Lỗi thường gặp

| Triệu chứng                                     | Nguyên nhân và cách xử lý                                                             |
| ----------------------------------------------- | ------------------------------------------------------------------------------------- |
| `not a git repository`                          | Đang đứng sai thư mục, hoặc chưa `git init`. Chạy `pwd` để kiểm tra                   |
| `command not found: python` hoặc thiếu thư viện | Chưa `conda activate tmdt`                                                            |
| `No module named 'rest_framework'`              | Chưa `pip install -r backend/requirements.txt` trong môi trường `tmdt`                |
| `no such table: ...`                            | Chưa chạy `python manage.py migrate`                                                  |
| `cannot import name 'Product'`                  | File `models.py` bị trống hoặc thiếu class. Mở file kiểm tra                          |
| Postman báo `Could not send request`            | Thiếu `http://127.0.0.1:8000` trong địa chỉ, hoặc `runserver` chưa chạy               |
| 401 Unauthorized                                | Thiếu header `Authorization: Token <token>`, hoặc token sai                           |
| 403 Forbidden                                   | Tài khoản không có quyền staff, hãy dùng tài khoản tạo bằng `createsuperuser`         |
| 400 khi đăng nhập `Unable to log in...`         | Sai tên đăng nhập hoặc mật khẩu. Đặt lại bằng `python manage.py changepassword <tên>` |
| Dán nhiều dòng vào terminal bị lỗi              | Dán từng khối một, hoặc mở file bằng VS Code, dán nội dung vào và lưu                 |

---
