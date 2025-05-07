import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

base_url = "https://www.shl.com/products/product-catalog/?start={}&type=1&type=1"
MAX_ITEMS = 500  

def get_page_content(url):
    """Fetches the HTML content of the page."""
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_duration(product_url):
    """Extracts the duration of the product from its individual page."""
    try:
        content = get_page_content(product_url)
        if not content:
            return 0
        soup = BeautifulSoup(content, 'html.parser')
        duration_paragraphs = soup.find_all('p')
        for p in duration_paragraphs:
            if 'Approximate Completion Time in minutes' in p.get_text():
                match = re.search(r'(\d+)', p.get_text())
                if match:
                    return int(match.group(1))
        return 0
    except Exception as e:
        print(f"Error extracting duration from {product_url}: {e}")
        return 0

def extract_description(product_url):
    """Extracts the description of the product from its individual page."""
    try:
        content = get_page_content(product_url)
        if not content:
            return "N/A"
        soup = BeautifulSoup(content, 'html.parser')
        description_tag = soup.find('h4', string='Description')
        if description_tag:
            description_paragraph = description_tag.find_next('p')
            if description_paragraph:
                return description_paragraph.get_text(strip=True)
        return "N/A"
    except Exception as e:
        print(f"Error extracting description from {product_url}: {e}")
        return "N/A"

def extract_data_from_page(page_content):
    """Extracts product data from the HTML content of a single page."""
    soup = BeautifulSoup(page_content, 'html.parser')
    rows = soup.find_all('tr', {'data-entity-id': True})
    product_data = []

    for row in rows:
        try:
            a_tag = row.find('a', href=True)
            product_url = "https://www.shl.com" + a_tag['href'] if a_tag else ""
            description = a_tag.get_text(strip=True) if a_tag else "N/A"
            adaptive_support = 'Yes' if row.find('span', class_='catalogue__circle -yes') else 'No'
            remote_support = 'Yes' 
            test_types = [span.get_text(strip=True) for span in row.find_all('span', class_='product-catalogue__key')]
            duration = extract_duration(product_url)
            time.sleep(0.5)  
            description = extract_description(product_url)
            product_data.append({
                "url": product_url,
                "adaptive_support": adaptive_support,
                "description": description,
                "duration": duration,
                "remote_support": remote_support,
                "test_type": ", ".join(test_types)
            })
        except Exception as e:
            print(f"Error parsing row: {e}")
    
    return product_data

def extract_next_page_url(current_url):
    """Extracts the URL for the next page from the current URL by incrementing the 'start' value."""
    start_index = current_url.find('start=')
    if start_index == -1:
        return None
    
    start_value = int(current_url[start_index + 6:current_url.find('&', start_index)] if '&' in current_url[start_index:] else current_url[start_index + 6:])
    next_start = start_value + 12
    next_url = f"https://www.shl.com/products/product-catalog/?start={next_start}&type=1&type=1"
    
    return next_url

def scrape_limited_products(max_items=500):
    """Scrapes product data from multiple pages, handling pagination dynamically."""
    all_data = []
    current_url = base_url.format(0) 
    page_number = 0

    while len(all_data) < max_items:
        print(f"Scraping {current_url}... (Page {page_number + 1})")
        page_content = get_page_content(current_url)
        if not page_content:
            print("Failed to fetch page content.")
            break
        page_data = extract_data_from_page(page_content)
        if not page_data:
            print("No more data found. Stopping.")
            break
        remaining = max_items - len(all_data)
        all_data.extend(page_data[:remaining])
        current_url = extract_next_page_url(current_url)

        if current_url:
            page_number += 1
            time.sleep(1) 
        else:
            print("No next page found. Stopping.")
            break

    return all_data

def save_to_csv(data, filename="product_catalog.csv"):
    """Saves the scraped data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Saved {len(data)} rows to {filename}")

if __name__ == "__main__":
    limited_data = scrape_limited_products(MAX_ITEMS)
    save_to_csv(limited_data)
