import requests
from bs4 import BeautifulSoup

url = "https://vi.wikipedia.org/wiki/%C4%90%E1%BA%A1i_h%E1%BB%8Dc_Qu%E1%BB%91c_gia_H%C3%A0_N%E1%BB%99i"
output_filename = "data_vnu_wikipedia_ver_1.1.txt"

try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    with open(output_filename, "w", encoding="utf-8") as f:
        page_title = soup.title.string if soup.title else "Không tìm thấy tiêu đề"
        
        content = soup.find("div", {"id": "mw-content-text"})
        
        current_topic = ""
        current_description = []
        
        for element in content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol']):
            if element.name.startswith('h'):
                if current_topic and current_description:
                    description_text = " ".join(current_description)
                    f.write(f"{page_title}:{current_topic}:{description_text}\n")
                
                current_topic = element.get_text(strip=True)
                current_description = []
                
                if current_topic.lower() == "xem thêm":
                    break
            
            elif element.name == 'p':
                text = element.get_text(strip=True)
                if text:
                    current_description.append(text)
            
            elif element.name in ['ul', 'ol']:
                list_items = []
                for li in element.find_all('li'):
                    item_text = li.get_text(strip=True)
                    list_items.append(item_text)
                
                if list_items:
                    list_text = ", ".join(list_items)
                    current_description.append(list_text)
        
        if current_topic and current_description:
            description_text = " ".join(current_description)
            f.write(f"{page_title}:{current_topic}:{description_text}\n")
    
    print(f"Đã thu thập dữ liệu và lưu vào file '{output_filename}'")

except requests.exceptions.RequestException as e:
    print(f"Lỗi khi tải trang: {e}")
except Exception as e:
    print(f"Lỗi khi phân tích cú pháp hoặc ghi file: {e}")