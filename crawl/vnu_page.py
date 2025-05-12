import requests
from bs4 import BeautifulSoup
import re
import os
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def clean_text(text):
    """Clean text by removing extra whitespace and special characters"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'\<.*?\>', '', text)  # Remove HTML tags if any remain
    return text.strip()

def scrape_vnu_website(url, file):
    """
    Function to scrape data from a VNU website page and save it to a text file.
    Args:
        url (str): URL of the VNU website
        file (file object): Opened file object to append data
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        logger.info(f"Attempting to connect to {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            logger.info(f"Successfully retrieved the website content (Status Code: {response.status_code})")
            soup = BeautifulSoup(response.text, 'html.parser')
            file.write(f"\n{'='*80}\n")
            file.write(f"URL: {url}\n")
            # Extract and write the title
            title = soup.title.string if soup.title else "ĐẠI HỌC QUỐC GIA HÀ NỘI"
            file.write(f"TITLE: {title}\n\n")
            # Extract and write meta description
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                file.write(f"DESCRIPTION: {meta_desc.get('content')}\n\n")
            # Extract main navigation menu items with submenus
            file.write("===== MENU CHÍNH =====\n")
            main_menu = soup.select('.dropdown > li')
            for menu_item in main_menu:
                menu_title = menu_item.select_one('span.down')
                if menu_title:
                    file.write(f"• {menu_title.text.strip()}\n")
                    sub_menu = menu_item.select('ul.sub_menu > li > a')
                    for sub_item in sub_menu:
                        file.write(f"  ├─ {sub_item.text.strip()}\n")
            file.write("\n")
            # Extract "Giới thiệu về đào tạo" content
            file.write("===== GIỚI THIỆU VỀ ĐÀO TẠO =====\n")
            training_section = soup.select_one('.catcontent')
            if training_section:
                section_title = training_section.select_one('.news-title')
                if section_title:
                    file.write(f"🔹 {section_title.text.strip()}\n\n")
                paragraphs = training_section.select('p')
                for p in paragraphs:
                    text = clean_text(p.text)
                    if text:
                        file.write(f"{text}\n\n")
            else:
                main_content = soup.select_one('.news-show') or soup.select_one('.catcontentmorther')
                if main_content:
                    paragraphs = main_content.select('p')
                    for p in paragraphs:
                        text = clean_text(p.text)
                        if text:
                            file.write(f"{text}\n\n")
            # Extract education programs
            file.write("===== CHƯƠNG TRÌNH ĐÀO TẠO =====\n")
            education_programs = soup.select('.catmenu .title-fix a')
            for program in education_programs:
                program_text = clean_text(program.text)
                if program_text:
                    file.write(f"• {program_text}\n")
            file.write("\n")
            # Extract featured news articles
            file.write("===== TIN TỨC NỔI BẬT =====\n")
            news_items = soup.select('.news-title-cate a') or soup.select('.title-cate a')
            if news_items:
                for i, news in enumerate(news_items[:10], 1):
                    news_title = clean_text(news.text)
                    news_link = news.get('href', '')
                    if news_link and not news_link.startswith(('http://', 'https://')):
                        news_link = url + news_link.lstrip('/')
                    file.write(f"{i}. {news_title}\n   Link: {news_link}\n")
            else:
                file.write("Không tìm thấy tin tức nổi bật.\n")
            file.write("\n")
            # Extract contact information
            file.write("===== THÔNG TIN LIÊN HỆ =====\n")
            contact_info = soup.select('.sub-menu li a')
            if contact_info:
                for contact in contact_info:
                    contact_text = clean_text(contact.text)
                    if contact_text:
                        file.write(f"• {contact_text}\n")
            else:
                file.write("Không tìm thấy thông tin liên hệ chi tiết.\n")
            logger.info(f"Data for {url} has been saved.")
        else:
            logger.error(f"Failed to retrieve the website content. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred during the request: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        logger.info("Starting VNU website scraper for multiple pages")
        with open('link_page_vnu.txt', 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f if line.strip()]
        with open('data_vnu_page.txt', 'w', encoding='utf-8') as file:
            for idx, url in enumerate(links, 1):
                logger.info(f"Scraping page {idx}/{len(links)}: {url}")
                scrape_vnu_website(url, file)
                time.sleep(2)  # Pause between requests
        logger.info("Web scraping for all pages completed successfully")
    except Exception as e:
        logger.error(f"Main execution error: {e}", exc_info=True)