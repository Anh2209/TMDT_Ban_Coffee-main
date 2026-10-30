# Đồ án TMĐT: Mô tả bài toán và phạm vi MVP (bản nháp 1)

Trạng thái: nháp, nhóm cần xem lại và chỉnh theo ý mình. Cập nhật 20/10/2026.

## 1. Đề tài
Xây dựng hệ thống thương mại điện tử bán lẻ cà phê tích hợp truy xuất và giám sát mẻ rang bằng IoT.

- Hướng đồ án: Hướng 1 (MVP hệ thống TMĐT), có thêm một module IoT dùng dữ liệu mô phỏng.
- Mô hình: B2C.
- Người bán: một cơ sở rang duy nhất (không phải marketplace).
- Cần xác nhận với thầy: "Hướng 1 làm chính, thêm module mô phỏng IoT truy xuất mẻ rang" có được chấp nhận không.

## 2. Vấn đề thực tế (viết lại)
Người mua cà phê rang online không kiểm chứng được cà phê được rang khi nào, rang ở mức nào, có đúng như quảng cáo không. Cơ sở rang nhỏ thì khó chứng minh chất lượng để cạnh tranh với thương hiệu lớn. Hệ thống giải quyết bằng cách gắn mỗi sản phẩm với một mẻ rang có dữ liệu giám sát, để khách tự xem và tin. "Bán được nhiều hơn" là kết quả mong đợi, không phải bài toán.

## 3. Người dùng
- Khách hàng (người uống cà phê tại nhà): tìm, chọn, đặt mua, theo dõi đơn, xem truy xuất mẻ rang.
- Chủ cơ sở rang / quản trị: quản lý sản phẩm, tồn kho, đơn hàng, tạo và gắn mẻ rang vào sản phẩm.
- Thiết bị rang (mô phỏng): gửi dữ liệu nhiệt độ theo thời gian về hệ thống.

## 4. Phạm vi MVP
Luồng bắt buộc (theo yêu cầu thầy: tìm kiếm, chọn sản phẩm, đặt hàng, checkout, theo dõi trạng thái):
1. Xem danh sách và tìm kiếm cà phê (lọc theo loại hạt, mức rang, giá).
2. Xem chi tiết sản phẩm.
3. Giỏ hàng.
4. Đặt hàng và thanh toán (mô phỏng cổng thanh toán).
5. Theo dõi trạng thái đơn hàng.
6. Quản trị: sản phẩm, tồn kho, đơn hàng.

Điểm khác biệt (IoT mô phỏng):
7. Mỗi sản phẩm/lô hàng gắn một mã mẻ rang.
8. Trang truy xuất (quét QR hoặc nhập mã): ngày rang, mức rang, đường cong nhiệt độ, độ tươi còn lại.
9. Module mô phỏng thiết bị rang gửi dữ liệu nhiệt độ qua API.
10. Quản trị tạo mẻ rang, xem giám sát, cảnh báo nếu nhiệt độ ngoài ngưỡng.

Để dành nếu còn thời gian: voucher, đánh giá sản phẩm, đơn vị vận chuyển, đăng nhập nâng cao.

Ngoài phạm vi: mua thiết bị thật, marketplace nhiều người bán, thanh toán thật, ứng dụng di động riêng.

## 5. Liên hệ kiến thức đã học
- API-first, REST, tách frontend và backend (Buổi 5, TH2 Hoppscotch).
- Chu trình IoT: Things, Sensors, Cloud, Intelligence, Decision, Action (Bài 4).
- Lòng tin khi mua online (Buổi 1), E-E-A-T và dữ liệu có cấu trúc cho SEO/GEO (Buổi 2).
- Backend kiểm tra giá, tồn kho, hợp lệ dữ liệu; không để frontend quyết (TH2, TH3).

## 6. Yêu cầu nộp của thầy
- Slide thuyết minh (chứa sơ đồ và hình), demo, báo cáo tối đa 5 trang Word chỉ có chữ, trả lời mục tiêu đồ án.
- Một bản báo cáo mỗi nhóm, gửi email qua đại diện.
- Quy định AI: chép nguyên văn nội dung AI thì cả nhóm 0 điểm; ý tưởng gốc phải của nhóm.
- Làm việc nhóm 5%, thành viên chấm chéo.

## 7. Việc tiếp theo
1. Nhóm xác nhận phạm vi MVP này.
2. Nhắn hỏi thầy về việc kết hợp module IoT mô phỏng.
3. Chọn công nghệ (ngôn ngữ, CSDL) theo năng lực nhóm. Đã chốt: Django + DRF, React + Vite + Chart.js.
4. Thiết kế kiến trúc, CSDL, API.
5. Phân công và lập lịch.
