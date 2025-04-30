from bs4 import BeautifulSoup
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  


def process_file(file_path):
    products = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        soup = BeautifulSoup(content, 'lxml')  # استخدام lxml لتحسين الأداء
        product_containers = soup.find_all('article', class_="prd _fb col c-prd")

        for product in product_containers:
            try:
                title = product.find('h3', class_="name").text.strip()
                price = product.find('div', class_="prc").text.strip()
                link = product.find('a', class_="core")['href']
                full_link = f"https://www.jumia.dz{link}"

                products.append({
                    "title": title,
                    "price": price,
                    "link": full_link
                })
            except Exception as e:
                pass  

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    
    return products


def scrape_saved_pages_parallel(folder_path, max_workers=8):
    
    all_products = []

    files = [os.path.join(folder_path, file_name) 
             for file_name in sorted(os.listdir(folder_path)) if file_name.endswith(".html")]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(tqdm(executor.map(process_file, files), total=len(files), desc="Processing files"))

    for product_list in results:
        all_products.extend(product_list)

    return all_products


folder_path = "jumia_pages"

products = scrape_saved_pages_parallel(folder_path)

df = pd.DataFrame(products)
df.to_csv("jumia_products_from_saved_pages.csv", index=False)
print(f"Data saved to jumia_products_from_saved_pages.csv. Extracted {len(products)} products.")
