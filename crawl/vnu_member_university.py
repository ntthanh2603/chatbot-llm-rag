import requests
from bs4 import BeautifulSoup
import time
import sys
import os
import urllib3 # Thư viện cần thiết để tắt cảnh báo SSL

# --- Cấu hình ---
INPUT_FILE = 'link_vnu_member_university.txt'  # Tên file chứa danh sách URL
OUTPUT_FILE = 'data_vnu_member_university.txt' # Tên file đầu ra
DELAY_SECONDS = 2 # Thời gian chờ giữa các yêu cầu
TIMEOUT_SECONDS = 15 # Thời gian chờ tối đa cho mỗi yêu cầu HTTP

# --- CẤU HÌNH XÁC MINH SSL ---
# Đặt THU_THAP_VOI_SSL_AN_TOAN = True nếu bạn muốn xác minh chứng chỉ SSL (mặc định và được khuyến nghị)
# Đặt THU_THAP_VOI_SSL_AN_TOAN = False để bỏ qua lỗi xác minh chứng chỉ SSL (kém an toàn hơn!)
THU_THAP_VOI_SSL_AN_TOAN = False # Thay đổi thành False để khắc phục lỗi SSLError

# Tắt cảnh báo khi xác minh SSL bị tắt
if not THU_THAP_VOI_SSL_AN_TOAN:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print("!!! CẢNH BÁO: Đã tắt xác minh chứng chỉ SSL. Kết nối có thể không an toàn. !!!")


# --- Hàm chính ---
def scrape_university_data(input_file, output_file, delay, timeout, verify_ssl):
    """
    Đọc URL từ file đầu vào, thu thập dữ liệu từ mỗi URL
    và ghi vào file đầu ra.
    verify_ssl: True để xác minh chứng chỉ SSL, False để bỏ qua lỗi SSL.
    """
    urls = []
    # 1. Đọc danh sách URL từ file đầu vào
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Đọc từng dòng, loại bỏ khoảng trắng thừa và dòng trống
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file đầu vào '{input_file}'. Vui lòng tạo file này và thêm các URL vào.")
        sys.exit(1)
    except Exception as e:
        print(f"Lỗi khi đọc file đầu vào '{input_file}': {e}")
        sys.exit(1)

    if not urls:
        print(f"Cảnh báo: File đầu vào '{input_file}' trống hoặc không chứa URL hợp lệ.")
        sys.exit(0)

    print(f"Đã đọc {len(urls)} URL từ '{input_file}'. Bắt đầu quá trình thu thập dữ liệu...")
    if not verify_ssl:
         print("Lưu ý: Đang thu thập dữ liệu với xác minh SSL bị tắt.")


    # 2. Mở file đầu ra để ghi dữ liệu (ghi đè nếu file đã tồn tại)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Duyệt qua từng URL trong danh sách
        for i, url in enumerate(urls):
            print(f"[{i+1}/{len(urls)}] Đang xử lý: {url}")

            # Thêm thời gian chờ giữa các request (trừ request đầu tiên)
            if i > 0:
                time.sleep(delay)

            try:
                # 3. Gửi yêu cầu HTTP để lấy nội dung trang
                # Thêm timeout để tránh bị treo vô thời hạn
                # >>> Thêm verify=verify_ssl vào đây <<<
                response = requests.get(url, timeout=timeout, verify=verify_ssl)

                # Kiểm tra mã trạng thái HTTP (ví dụ: 404, 500).
                response.raise_for_status()

                # 4. Phân tích nội dung HTML bằng BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # 5. Trích xuất dữ liệu (toàn bộ nội dung văn bản)
                scraped_data = soup.get_text(separator='\n', strip=True)

                # 6. Ghi dữ liệu đã thu thập vào file đầu ra
                outfile.write(f"--- Dữ liệu từ: {url} ---\n")
                outfile.write(scraped_data)
                outfile.write("\n\n") # Thêm 2 dòng trống để phân tách

                print(f"  -> Thu thập thành công.")

            except requests.exceptions.MissingSchema:
                print(f"  -> Lỗi: URL không hợp lệ (thiếu schema). Bỏ qua: {url}")
                outfile.write(f"--- LỖI URL không hợp lệ (thiếu schema): {url} ---\n\n")
            except requests.exceptions.ConnectionError as e:
                print(f"  -> Lỗi kết nối khi truy cập {url}: {e}")
                outfile.write(f"--- LỖI kết nối: {url} ---\n\n")
            except requests.exceptions.Timeout:
                 print(f"  -> Lỗi timeout khi truy cập {url}.")
                 outfile.write(f"--- LỖI timeout: {url} ---\n\n")
            except requests.exceptions.HTTPError as e:
                print(f"  -> Lỗi HTTP khi truy cập {url}: {e}")
                outfile.write(f"--- LỖI HTTP: {url} ({e}) ---\n\n")
            except requests.exceptions.SSLError as e:
                 # Xử lý riêng lỗi SSL nếu verify=True nhưng vẫn xảy ra lỗi khác
                 print(f"  -> Lỗi SSL khi truy cập {url}: {e}")
                 outfile.write(f"--- LỖI SSL: {url} ({e}) ---\n\n")
            except Exception as e:
                print(f"  -> Lỗi không xác định khi xử lý {url}: {e}")
                outfile.write(f"--- LỖI không xác định: {url} ({e}) ---\n\n")

    print(f"\nHoàn tất quá trình thu thập dữ liệu.")
    print(f"Dữ liệu đã được lưu vào file '{output_file}'.")

# --- Điểm bắt đầu chạy script ---
if __name__ == "__main__":
    # Truyền cấu hình xác minh SSL vào hàm
    scrape_university_data(INPUT_FILE, OUTPUT_FILE, DELAY_SECONDS, TIMEOUT_SECONDS, THU_THAP_VOI_SSL_AN_TOAN)