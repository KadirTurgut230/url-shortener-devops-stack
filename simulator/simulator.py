import time
import random
import requests
from config import settings

TARGET_URLS = [
    "https://github.com/torvalds/linux",
    "https://hub.docker.com",
    "https://www.postgresql.org/docs/",
    "https://fastapi.tiangolo.com/"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B)"
]

FAKE_IPS = ["85.105.12.34", "185.220.101.5", "104.28.15.2", "176.240.10.11"]

def wait_for_api():
    print(f"API servisi ({settings.API_URL}) bekleniyor...")
    while True:
        try:
            requests.get(f"{settings.API_URL}/docs", timeout=2)
            print("API ayakta, simülasyon başlıyor!")
            break
        except requests.exceptions.RequestException:
            time.sleep(3)

def generate_short_links():
    short_codes = []
    print("Test linkleri oluşturuluyor...")
    for url in TARGET_URLS:
        try:
            response = requests.post(f"{settings.API_URL}/shorten", json={"original_url": url})
            if response.status_code == 200:
                code = response.json().get("short_code")
                short_codes.append(code)
                print(f"Oluşturuldu: {code}")
        except Exception as e:
            pass
    return short_codes

def run_simulation(short_codes):
    print("Yapay trafik üretimi başlatıldı...")
    while True:
        code = random.choice(short_codes)
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "X-Forwarded-For": random.choice(FAKE_IPS)
        }
        try:
            requests.get(f"{settings.API_URL}/{code}", headers=headers, allow_redirects=False)
            print(f"[TIK] /{code} adresine tıklandı. (IP: {headers['X-Forwarded-For']})")
        except Exception:
            pass
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    wait_for_api()
    codes = generate_short_links()
    if codes:
        run_simulation(codes)

