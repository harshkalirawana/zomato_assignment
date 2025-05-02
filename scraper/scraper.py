import requests, re, io, time, json
from bs4 import BeautifulSoup
import html2text
import cohere
import pdfplumber
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Setup
CO_API_KEY = "2j4Ag4jjCJAR0u28GhhbP0PL3wBUWFqJEvL8NaOr"
co = cohere.Client(CO_API_KEY)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.google.com",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_html_text(url):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        for tag in soup(['script', 'style']):
            tag.decompose()
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images = True
        return text_maker.handle(str(soup)), soup
    except Exception as e:
        return f"Error fetching HTML: {e}", None

def find_media(soup, base_url):
    images, pdfs = [], []
    for img in soup.find_all("img", src=True):
        src = img['src']
        if "menu" in src.lower():
            images.append(urljoin(base_url, src))
    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.endswith(".pdf"):
            pdfs.append(urljoin(base_url, href))
    return images, pdfs

def extract_text_from_images(image_urls):
    text = ""
    for img_url in image_urls:
        try:
            print(f"🖼️ Extracting image: {img_url}")
            img_data = requests.get(img_url, timeout=10).content
            img = Image.open(io.BytesIO(img_data))
            text += pytesseract.image_to_string(img)
        except Exception as e:
            text += f"\n[Image Error: {e}]"
    return text

def extract_text_from_pdfs(pdf_urls):
    full_text = ""
    for pdf_url in pdf_urls:
        try:
            print(f"📄 Extracting PDF: {pdf_url}")
            r = requests.get(pdf_url, timeout=10)
            r.raise_for_status()
            with pdfplumber.open(io.BytesIO(r.content)) as pdf:
                for page in pdf.pages:
                    full_text += page.extract_text() or ""
            if not full_text.strip():
                images = convert_from_bytes(r.content)
                for img in images:
                    full_text += pytesseract.image_to_string(img)
        except Exception as e:
            full_text += f"\n[PDF Error: {e}]"
    return full_text

def extract_dynamic_menu(url):
    print("🌐 Launching headless browser to capture JS-rendered menu...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)  # Wait for JS to load; adjust if needed

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    menu_text = ""
    try:
        menu_sections = soup.find_all("div", {"class": re.compile(r"sc-.*-0.*")})
        for section in menu_sections:
            if "₹" in section.text:
                menu_text += section.get_text(separator="\n") + "\n"
    except Exception as e:
        menu_text += f"\n[Selenium Parsing Error: {e}]"

    driver.quit()
    return menu_text

def extract_info_from_text(text):
    prompt = f"""
You are an intelligent parser that extracts structured data from messy or unstructured web-scraped restaurant content.

From the text below, extract and return a clean, well-formatted JSON object that includes:
- restaurant_name: Name of the restaurant.
- location: Full address or city/location.
- operating_hours: Operating days and hours.
- contact_info: Include phone number, email, full address, and any available social media or website links.
- menu_items: A list of maximum 100 menu items. Each item should include:
  - name
  - description (if available)
  - price
- special_features: Highlight features like vegetarian options, spice levels, allergen info, or anything unique.
- reviews: A list of maximum 10 reviews, each with:
  - star_rating (e.g., 4.5/5)
  - reviewer_name
  - comment
  - date

Make the JSON clean, human-readable, and as complete and accurate as possible based on the text provided.

Text:
{text}
"""

    try:
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=20000,
            temperature=0.3
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"LLM Error: {e}"

def extract_zomato_data(base_url):
    all_text = ""

    # 1. Info Page
    info_url = base_url.rstrip("/") + "/info"
    info_text, soup_info = fetch_html_text(info_url)
    all_text += f"\n[INFO SECTION]\n{info_text}\n"

    # 2. Menu Page (/order)
    menu_url = base_url.rstrip("/") + "/order"
    static_menu_text, soup_menu = fetch_html_text(menu_url)
    dynamic_menu_text = extract_dynamic_menu(menu_url)
    all_text += f"\n[MENU SECTION - STATIC]\n{static_menu_text}\n"
    all_text += f"\n[MENU SECTION - DYNAMIC]\n{dynamic_menu_text}\n"

    # OCR/PDFa
    image_urls, pdf_urls = find_media(soup_menu, menu_url)
    ocr_text = extract_text_from_images(image_urls)
    pdf_text = extract_text_from_pdfs(pdf_urls)
    all_text += f"\n[MENU OCR TEXT]\n{ocr_text}\n{pdf_text}\n"

    # 3. Reviews Page
    reviews_url = base_url.rstrip("/") + "/reviews"
    reviews_text, _ = fetch_html_text(reviews_url)
    all_text += f"\n[REVIEWS SECTION]\n{reviews_text}\n"

    # Run through AI model
    print("🧠 Sending to AI for structuring...")
    return extract_info_from_text(all_text[:90000])  # max token cap

def convert_to_json(result_string):
    """
    Convert the LLM's text output to proper JSON format

    Args:
        result_string (str): The raw output from the LLM

    Returns:
        dict: The parsed JSON data or error object
    """
    import json
    import re

    def sanitize_json_string(s):
        # Remove markdown code block syntax
        s = s.strip()
        if s.startswith("```json"):
            s = s[7:]
        if s.endswith("```"):
            s = s[:-3]
        s = s.strip()

        # Remove comments (// or /* */)
        s = re.sub(r'//.*', '', s)
        s = re.sub(r'/\*.*?\*/', '', s, flags=re.DOTALL)

        # Convert single quotes to double quotes (carefully)
        s = re.sub(r"(?<!\\)'", '"', s)

        # Fix trailing commas
        s = re.sub(r',\s*([}\]])', r'\1', s)

        # Add quotes to unquoted keys (basic heuristic, won't catch all cases)
        s = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)\s*:', r'\1"\2":', s)

        return s

    clean_string = sanitize_json_string(result_string)

    try:
        return json.loads(clean_string)
    except json.JSONDecodeError as e:
        print(f"❌ Final JSON parse failed: {e}")
        return {"error": "Could not parse the result into valid JSON format"}

def save_json_to_file(json_data, filename):
    """
    Save the JSON data to a file

    Args:
        json_data (dict): The JSON data to save
        filename (str): The name of the file to save to
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"JSON data saved to {filename}")

# === USAGE ===
if __name__ == "__main__":
    # Get the restaurant URL from user input
    url = "https://www.zomato.com/kharagpur/super-duper-cafe-iit-kharagpur"

    # Extract the restaurant data
    print(f"Extracting data from {url}...")
    result_string = extract_zomato_data(url)

    # Convert the result to JSON
    print("Converting to JSON format...")
    json_data = convert_to_json(result_string)

    # Display a pretty-printed preview of the JSON data
    print("\n📊 JSON Preview:")
    print(json.dumps(json_data, indent=2, ensure_ascii=False)[:1000] + "...\n")

    # Save to file
    restaurant_name = json_data.get('restaurant_name', 'restaurant').lower().replace(' ', '_')
    filename = f"{restaurant_name}_data.json"
    save_json_to_file(json_data, filename)

    print(f"Processing completed for {json_data.get('restaurant_name', 'restaurant')}")
    print(f"Full details saved to {filename}")