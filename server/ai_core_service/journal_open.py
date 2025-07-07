import requests
import pandas as pd
import os
import time
import random
from dotenv import load_dotenv
load_dotenv()

CORE_API_KEY = os.environ.get("CORE_API_KEY")
if not CORE_API_KEY:
    raise ValueError("CORE_API_KEY not set in environment or .env file.")
QUERY = "Battery SoC and SoH estimation using deep learning"
OUTPUT_DIR = "core_downloads"
PAGE_SIZE = 10  # You can set this up to 100 per the API docs

def download_file(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def fetch_core_page(query, page, page_size):
    base_url = "https://api.core.ac.uk/v3/search/works"
    headers = {"Authorization": f"Bearer {CORE_API_KEY}"}
    params = {
        "q": query,
        "page": page,
        "pageSize": page_size,
        "fulltext": "true"
    }
    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def fetch_all_core_results(query, page_size=10, max_pages=None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_records = []
    page = 1
    while True:
        print(f"Fetching page {page}...")
        try:
            data = fetch_core_page(query, page, page_size)
        except requests.HTTPError as e:
            print(f"Error: {e}")
            break
        results = data.get("results", [])
        if not results:
            print("No more results.")
            break
        for idx, work in enumerate(results):
            title = work.get("title", "")
            abstract = work.get("abstract", "")
            download_url = work.get("downloadUrl", "")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{OUTPUT_DIR}/{page}_{idx}_{safe_title[:50]}.pdf" if download_url else ""
            record = {
                "title": title,
                "abstract": abstract,
                "download_url": download_url,
                "filename": filename
            }
            if download_url:
                try:
                    download_file(download_url, filename)
                    print(f"Downloaded: {filename}")
                except Exception as e:
                    print(f"Failed to download {download_url}: {e}")
                    record["filename"] = ""
            all_records.append(record)
        page += 1
        if max_pages and page > max_pages:
            break
        time_sleep = random.randint(10, 60)
        print(f"Sleeping for {time_sleep} seconds to respect rate limits...")
        time.sleep(time_sleep) # Random sleep to avoid hitting API rate limits
    return pd.DataFrame(all_records)

def fetch_all_core_results_api(query, page_size=10, max_pages=5):
    try:
        df = fetch_all_core_results(query, page_size=page_size, max_pages=max_pages)
        records = df.to_dict(orient='records')
        return {"status": "success", "records": records, "num_records": len(records)}
    except Exception as e:
        return {"status": "error", "error": str(e), "records": []}

if __name__ == "__main__":
    df = fetch_all_core_results(QUERY, page_size=PAGE_SIZE, max_pages=5)
    print(f"Total records fetched: {len(df)}")
    print(df.head())
    df.to_csv("core_results.csv", index=False)
