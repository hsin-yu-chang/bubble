import re
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote

input_file = Path("messages.json")
output_dir = Path("cloudinary_images")
output_dir.mkdir(exist_ok=True)

text = input_file.read_text(encoding="utf-8")

# 抓出 "url":"https://..."
urls = re.findall(r'"url"\s*:\s*"([^"]+)"', text)

# 去重，但保留原本順序
urls = list(dict.fromkeys(urls))

print(f"抓到 {len(urls)} 個 URL")

# 先處理成原畫質網址
def remove_cloudinary_options(url: str) -> str:
    replacements = [
        "/image/upload/q_auto,f_auto,fl_lossy/",
        "/image/upload/f_auto,q_auto/",
        "/image/upload/q_auto,f_auto/",
        "/video/upload/f_auto,q_auto/",
        "/video/upload/q_auto,f_auto/",
    ]

    for old in replacements:
        if old in url:
            return url.replace(old, old.split("/upload/")[0] + "/upload/")

    return url
clean_urls = [
    remove_cloudinary_options(url)
    for url in urls
]

print("\n以下是準備下載的網址：")
for index, clean_url in enumerate(clean_urls, start=1):
    print(f"{index}. {clean_url}")

input("\n確認要下載請按 Enter；不想下載就按 Ctrl + C 中止：")

for index, clean_url in enumerate(clean_urls, start=1):
    parsed = urlparse(clean_url)
    filename = unquote(Path(parsed.path).name)

    if not filename:
        filename = f"image_{index}.jpg"

    save_path = output_dir / filename

    try:
        response = requests.get(clean_url, timeout=30)
        response.raise_for_status()

        save_path.write_bytes(response.content)
        print(f"[OK] {filename}")

    except Exception as e:
        print(f"[失敗] {clean_url}")
        print(f"原因：{e}")

print("下載完成")