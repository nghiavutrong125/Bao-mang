# Hướng Dẫn Xử Lý Ảnh & Cloudflare R2 - Fifty Fifty Magazine

Hệ thống xử lý ảnh và đồng bộ Cloudflare R2 độc lập cho dự án **Fifty Fifty Magazine**.

---

## 1. Thông Tin Cấu Hình R2 & CDN
* **Cloudflare Bucket:** `bao-mang`
* **Remote Rclone:** `r2-baomang:bao-mang`
* **Thư mục lưu trữ máy tính:** `D:\Anh_Cloud\fiftyfifty-data`
* **Tên miền Public CDN:** `https://pub-a444990dcfe849f3bdc97bf8dc4ca482.r2.dev`

---

## 2. Đặc Điểm Kỹ Thuật
1. **Xóa sạch 100% EXIF Metadata:** Không lưu camera model, tọa độ GPS, ngày giờ chụp, phần mềm chỉnh sửa.
2. **Không Watermark / Không gắn logo:** Giữ nguyên nét tự nhiên, chuẩn báo chí quốc tế.
3. **Định dạng tối ưu:** Chuyển sang WebP (Quality 85, nén sâu <150KB, hiển thị sắc nét).
4. **Tự động đặt tên:** Tự chuyển tên sang tiếng Anh chuẩn SEO dạng `ha-giang-loop-01.webp`, `ha-giang-loop-02.webp`.

---

## 3. Cách Sử Dụng

### Cách 1: Nhờ AI Agent (Tiện lợi nhất)
Bạn chỉ cần gửi file ảnh hoặc đường dẫn thư mục ảnh bất kỳ cho tôi kèm tên bài viết:
> *"Xử lý loạt ảnh này cho bài 'Da Nang Hidden Cafes'"*
Tôi sẽ tự động chạy pipeline, nén ảnh, xóa sạch dấu vết kỹ thuật, đẩy lên R2 và nhúng thẳng link vào bài viết cho bạn.

### Cách 2: Chạy file 1-Click (XU-LY-ANH.bat)
1. Copy ảnh cần xử lý vào thư mục `photos-raw/`.
2. Nhấp đúp vào file `XU-LY-ANH.bat`.
3. Nhập tên SEO và chọn tỷ lệ ảnh.
4. Tool sẽ tự nén, lưu trữ bản sao ở `D:\Anh_Cloud\fiftyfifty-data` và đẩy thẳng lên Cloudflare R2.

