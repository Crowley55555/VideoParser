import logging
import os
import re
import sys
import threading
import requests
import yt_dlp
from urllib.parse import urlparse

# Консоль Windows: вывод в UTF-8, чтобы русский текст отображался
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

YOUTUBE_PATTERN = re.compile(
    r"(https?://)?(www\.)?(youtube\.com|youtu\.be|youtube-nocookie\.com)/"
)

# Логи: в файл и в консоль
LOG_FILE = os.path.join(os.path.dirname(__file__), "videoparser.log")
_log = logging.getLogger("VideoParser")
_log.setLevel(logging.DEBUG)
_fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
_fh.setLevel(logging.DEBUG)
_ch = logging.StreamHandler(sys.stdout)
_ch.setLevel(logging.INFO)
_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
_fh.setFormatter(_fmt)
_ch.setFormatter(_fmt)
_log.addHandler(_fh)
_log.addHandler(_ch)


def _is_youtube_url(url):
    return bool(YOUTUBE_PATTERN.match(url))


def _progress_hook(d):
    if d["status"] == "downloading":
        filename = os.path.basename(d.get("filename", ""))
        percent = d.get("_percent_str", "?%").strip()
        speed = d.get("_speed_str", "?").strip()
        eta = d.get("_eta_str", "").strip()
        down = d.get("_downloaded_bytes") or 0
        total = d.get("_total_bytes")
        size_str = f"{down / (1024*1024):.1f} MiB"
        if total and total > 0:
            size_str += f" / {total / (1024*1024):.1f} MiB"
        line = f"\r  -> {filename[:40]:<40} {percent} | {size_str} | {speed}"
        if eta:
            line += f" | ETA {eta}"
        print(line, end="", flush=True)
    elif d["status"] == "finished":
        filename = os.path.basename(d.get("filename", ""))
        print(f"\n[OK] Скачано: {filename}")
        _log.info("Скачано: %s", filename)
    elif d["status"] == "error":
        _log.error("Ошибка загрузки: %s", d.get("filename", ""))


def _download_youtube(url, save_dir, browser=None, cookiefile=None):
    os.makedirs(save_dir, exist_ok=True)
    ydl_opts = {
        "outtmpl": os.path.join(save_dir, "%(title)s.%(ext)s"),
        "format": "best",
        "progress_hooks": [_progress_hook],
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    if cookiefile and os.path.isfile(cookiefile):
        ydl_opts["cookiefile"] = cookiefile
        _log.debug("Используются куки: %s", cookiefile)
    elif browser:
        ydl_opts["cookiesfrombrowser"] = (browser,) if isinstance(browser, str) else tuple(browser)
        _log.debug("Куки из браузера: %s", browser)
    try:
        print(f"[>>] Загрузка YouTube: {url}")
        _log.info("Старт загрузки: %s", url)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"\n[!] Ошибка ({url}): {e}")
        _log.exception("Ошибка: %s", e)


def _download_direct(url, save_dir):
    filename = os.path.basename(urlparse(url).path) or f"file_{abs(hash(url)) % 10**8}"
    filepath = os.path.join(save_dir, filename)
    os.makedirs(save_dir, exist_ok=True)

    try:
        print(f"[>>] Начало загрузки: {filename}")
        _log.info("Прямая загрузка: %s", url)
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        total_mb = total_size / (1024 * 1024) if total_size else 0

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        down_mb = downloaded / (1024 * 1024)
                        print(
                            f"\r  -> {filename[:40]:<40} {percent:.1f}% | {down_mb:.1f} / {total_mb:.1f} MiB",
                            end="",
                            flush=True,
                        )
        print(f"\n[OK] Готово: {filename}")
        _log.info("Скачано: %s", filename)
    except Exception as e:
        print(f"\n[!] Ошибка ({filename}): {e}")
        _log.exception("Ошибка: %s", e)


def download_file(url, save_dir, browser=None, cookiefile=None):
    url = url.strip()
    if not url:
        return

    if _is_youtube_url(url):
        _download_youtube(url, save_dir, browser=browser, cookiefile=cookiefile)
    else:
        _download_direct(url, save_dir)


def download_files(urls, save_dir, max_threads=4, browser=None, cookiefile=None):
    semaphore = threading.Semaphore(max_threads)

    def _worker(link):
        with semaphore:
            download_file(link, save_dir, browser=browser, cookiefile=cookiefile)

    threads = []
    for url in urls:
        t = threading.Thread(target=_worker, args=(url,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("\n[OK] Все загрузки завершены.")
    _log.info("Все загрузки завершены. Лог: %s", LOG_FILE)
