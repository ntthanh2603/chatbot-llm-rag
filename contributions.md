# Đóng góp của các thành viên

Tài liệu này mô tả chi tiết đóng góp của từng thành viên trong nhóm trong các mảng:

- **Gán nhãn dữ liệu**
- **Thu thập và xử lý dữ liệu**
- **Xây dựng và triển khai mô hình**

---

## Thành viên nhóm

- **Tuấn Thành** (Nguyễn Tuấn Thành / 22022624)
- **Việt Anh** (Ngô Việt Anh / 22022508)
- **Nhật Tân** (Nguyễn Nhật Tân / 22022530)
- **Đăng Trường** (Chu Hữu Đăng Trường / 22022505)

---

## 1. Đóng góp trong việc gán nhãn dữ liệu

- **Tuấn Thành**: Gán nhãn các cặp câu hỏi-trả lời từ dòng 1–55 trong `data/test/`.
- **Việt Anh**: Gán nhãn các cặp câu hỏi-trả lời từ dòng 56–110 trong `data/test/`.
- **Nhật Tân**: Gán nhãn các cặp câu hỏi-trả lời từ dòng 111–165 trong `data/test/`.
- **Đăng Trường**: Kiểm tra lại các nhãn đã gán và tính toán độ đồng thuận giữa các người gán nhãn (Inter-Annotator Agreement - IAA) trên 30 ví dụ ngẫu nhiên từ tập test.

---

## 2. Đóng góp trong thu thập và xử lý dữ liệu

- **Tuấn Thành**: Viết script thu thập dữ liệu từ các trang chính thức của VNU và làm sạch HTML sử dụng `beautifulsoup4`.
- **Việt Anh**: Kiểm tra chất lượng dữ liệu, đồng thời loại bỏ nội dung không liên quan.
- **Nhật Tân**: Tổng hợp tài liệu thô thành định dạng có thể lập chỉ mục.
- **Đăng Trường**: Tạo tập hợp dữ liệu cuối cùng cho huấn luyện và kiểm thử, chuẩn hóa định dạng và tổ chức file theo cấu trúc thư mục yêu cầu.

---

## 3. Đóng góp trong xây dựng và phát triển hệ thống

- **Tuấn Thành**: Cài đặt bộ nhúng truy vấn và tài liệu sử dụng thư viện `sentence-transformers`, đồng thời xây dựng pipeline truy hồi tài liệu hiệu quả. Tuấn Thành cũng đảm nhiệm việc tối ưu hiệu suất của quá trình truy hồi nhằm đảm bảo hệ thống phản hồi nhanh và chính xác.
- **Việt Anh**: Phụ trách viết mã để hệ thống có thể xuất kết quả trên tập test theo định dạng yêu cầu. Ngoài ra, Việt Anh còn xây dựng các biểu đồ phân tích kết quả (ví dụ: phân bố độ chính xác, biểu đồ so sánh giữa các mô hình), nhằm hỗ trợ việc đánh giá định lượng và trực quan hóa hiệu suất của hệ thống.
- **Nhật Tân**: Chịu trách nhiệm xử lý phần đánh giá kết quả đầu ra của hệ thống thông qua các chỉ số phổ biến như Exact Match và F1-score. Bên cạnh đó, Nhật Tân hỗ trợ việc tinh chỉnh mô hình và đề xuất các phương pháp cải thiện chất lượng sinh câu trả lời.
- **Đăng Trường**: Tích hợp tất cả các module thành một hệ thống RAG hoàn chỉnh, đảm bảo các thành phần embedding, retrieval và generation phối hợp mượt mà. Đồng thời, Đăng Trường quản lý hệ thống cơ sở dữ liệu vector (PineconeDB), xử lý các vấn đề liên quan đến lập chỉ mục, đồng bộ dữ liệu và hiệu suất truy vấn.