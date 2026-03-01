import os
from parser import download_files

# ———————— Всё в одном месте ————————
SAVE_DIR = r"D:\data\1"
COOKIES_FILE = os.path.join(os.path.dirname(__file__), "cookies.txt")  # или None
BROWSER = "firefox"  # если cookies.txt нет

LINKS = [
    # "https://youtu.be/WcjQQLBHZTE?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/crzopwHY-tU?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/LwfuPoX9atI?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/N8C1Lh64-wQ?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/r6Dz9ThRzTM?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/2tGpn-bPpFI?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/s0_vVkZ9oGU?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/K1E6CBCzegI?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/6qxHhAcvXGQ?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/wrfPNaOj1Lc?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/79nCNUYgv0Y?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/40drwSD6NpQ?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/3UcYN6BuOzY?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/qKVfzNt1sLU?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/6vXA7aRwdoo?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/9jefwa7vuO4?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/218AIDUgTF4?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/fRTeG-8Zny8?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/XY2QF0R1tpE?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/NruLSRhCETQ?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/Vf-0pp8y6qE?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/ccaqNkpdc1Y?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/7Kfh62de0w0?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/yCa4Tz1Pqdk?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/Il3PLEt1ItA?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/rQwV8BmbgGU?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
    # "https://youtu.be/YFtvw0knXQM?list=PLrMP3FWJohmdsKhbj5vn5pBvf0mD8WIib",
]

if __name__ == "__main__":
    download_files(
        LINKS,
        save_dir=SAVE_DIR,
        cookiefile=COOKIES_FILE if COOKIES_FILE and os.path.isfile(COOKIES_FILE) else None,
        browser=BROWSER,
    )

