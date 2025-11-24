import os
import threading
import requests
from urllib.parse import urlparse

def download_file(url, save_dir):
    url = url.strip()
    if not url:
        return

    filename = os.path.basename(urlparse(url).path) or f"file_{abs(hash(url)) % 10**8}"
    filepath = os.path.join(save_dir, filename)
    os.makedirs(save_dir, exist_ok=True)

    try:
        print(f"📥 Начало загрузки: {filename}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=65536):  # 64KB
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r  → {filename[:50]:<50} {percent:.1f}%", end='', flush=True)
        print(f"\n✅ Готово: {filename}")
    except Exception as e:
        print(f"\n❌ Ошибка ({filename}): {e}")

def download_files(urls, save_dir):
    threads = []
    for url in urls:
        t = threading.Thread(target=download_file, args=(url, save_dir))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("\n✨ Все загрузки завершены.")

