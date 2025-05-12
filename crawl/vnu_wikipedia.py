import requests
from bs4 import BeautifulSoup

url = "https://vi.wikipedia.org/wiki/%C4%90%E1%BA%A1i_h%E1%BB%8dc_Qu%E1%BB%91c_gia_H%C3%A0_N%E1%BB%99i"
output_filename = "vnu_wikipedia.txt"

try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    with open(output_filename, "w", encoding="utf-8") as f:
        page_title = soup.title.string if soup.title else "Không tìm thấy tiêu đề"
        f.write(f"Tiêu đề trang: {page_title}\n\n")

        infobox = soup.find("table", {"class": "infobox"})
        if infobox:
            f.write("-- BẢNG THÔNG TIN (INFOBOX) --\n")
            for row in infobox.find_all("tr"):
                header = row.find("th")
                data = row.find("td")
                if header and data:
                    f.write(f"{header.get_text(strip=True)}: {data.get_text(strip=True)}\n")
            f.write("\n")

        content = soup.find("div", {"id": "mw-content-text"})
        for element in content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol']):
            if element.name.startswith('h'):
                heading_text = element.get_text(strip=True)

                if heading_text.lower() == "xem thêm":
                    break

                f.write(f"\n-- {heading_text} --\n")
            elif element.name == 'p':
                text = element.get_text(strip=True)
                if text:
                    f.write(text + "\n")
            elif element.name in ['ul', 'ol']:
                for li in element.find_all('li'):
                    item_text = li.get_text(strip=True)
                    f.write(f"- {item_text}\n")

    print(f"Đã thu thập dữ liệu và lưu vào file '{output_filename}'")

except requests.exceptions.RequestException as e:
    print(f"Lỗi khi tải trang: {e}")
except Exception as e:
    print(f"Lỗi khi phân tích cú pháp hoặc ghi file: {e}")
