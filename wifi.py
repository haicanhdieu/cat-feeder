import network
import uasyncio as asyncio
from ntp import sync_time_with_ntp

# ==== WiFi Connect ====
async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Read credentials from wifi.json
    ssid = ""
    password = ""
    try:
        import json
        with open("wifi.json", "r") as f:
            creds = json.load(f)
            ssid = creds.get("ssid", "")
            password = creds.get("password", "")
    except Exception as e:
        print("Could not read wifi.json:", e)
    if not wlan.isconnected():
        print("🔌 Connecting to WiFi... SSID:", ssid)
        wlan.connect(ssid, password)
        max_attempts = 10
        attempts = 0
        while not wlan.isconnected() and attempts < max_attempts:
            print("⏳ Waiting for WiFi...")
            await asyncio.sleep(1)
            attempts += 1

        if not wlan.isconnected():
            raise RuntimeError("Failed to connect to WiFi after 10 attempts")
    print("✅ Connected:", wlan.ifconfig())
    await sync_time_with_ntp()
    return wlan
