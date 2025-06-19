import requests

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150',
}

try:
    r = requests.get("https://check.torproject.org", proxies=proxies, timeout=15)
    print("✅ Tor работает!" if "Congratulations" in r.text else "⚠️ Tor не работает!")
except Exception as e:
    print("❌ Ошибка:", e)