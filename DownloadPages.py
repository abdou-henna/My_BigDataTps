import os
import requests
from time import sleep

def save_pages(base_url, save_folder, max_pages):
   
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    for page in range(1, max_pages + 1):
        print(f"Downloading page {page}...")
        url = f"{base_url}&page={page}"
        response = requests.get(url)
        
        if response.status_code == 200:
            file_path = os.path.join(save_folder, f"page_{page}.html")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"Page {page} saved as {file_path}.")
        else:
            print(f"Failed to download page {page}. Status code: {response.status_code}")
            break
        
        sleep(0)

    print("All pages downloaded!")

base_url = "https://www.jumia.com.dz/ordinateurs-accessoires-informatique/?q=ram#catalog-listing"

save_folder = "jumia_pages"

save_pages(base_url, save_folder, max_pages=10000)
