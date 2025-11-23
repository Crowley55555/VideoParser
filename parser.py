import requests
import os
from urllib.parse import urlparse

def download_file(url, save_dir='.'):
    # Получаем имя файла из URL
    filename = os.path.basename(urlparse(url).path)
    if not filename:
        filename = 'downloaded_file'

    # Полный путь к файлу
    filepath = os.path.join(save_dir, filename)

    # Создаём папку, если её нет
    os.makedirs(save_dir, exist_ok=True)

    print(f"Скачивание: {url}")
    print(f"Сохранение в: {os.path.abspath(filepath)}")

    # Потоковая загрузка
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Получаем общий размер файла (если указан)
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0

    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rПрогресс: {percent:.1f}%", end='', flush=True)
    print("\nЗагрузка завершена!")

# Пример использования:
# download_file("https://example.com/video.mp4", save_dir="./downloads")