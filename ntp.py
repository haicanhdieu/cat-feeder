import ntptime
import time
import uasyncio as asyncio

# Vietnam UTC+7
TIMEZONE_OFFSET = 7 * 3600  

def localtime():
    import time
    t = time.time() + TIMEZONE_OFFSET
    return time.localtime(t)

async def sync_time_with_ntp():
    ntptime.host = "162.159.200.1"  # Cloudflare NTP
    for attempt in range(3):
        try:
            ntptime.settime()
            print("✅ Time synchronized with NTP (UTC). Local:", localtime())
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(5)

    # ==== Fallback to HTTP ====
    print("⚠️ Falling back to HTTP time API...")
    try:
        import urequests, machine
        r = urequests.get("http://worldtimeapi.org/api/timezone/Asia/Ho_Chi_Minh")
        data = r.json()
        ts = int(data["unixtime"])
        rtc = machine.RTC()
        tm = time.localtime(ts)
        rtc.datetime((
            tm[0], tm[1], tm[2],
            tm[6], tm[3], tm[4], tm[5],
            0
        ))
        print("✅ Time synchronized via HTTP fallback:", localtime())
    except Exception as e:
        print("❌ Failed to get time from HTTP API:", e)
