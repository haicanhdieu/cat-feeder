import uasyncio as asyncio
import re
import json
from url_helper import url_decode
import machine

async def delayed_reset():
    await asyncio.sleep(5)
    machine.reset()

# ==== HTTP Handler ====
async def handle_client(reader, writer):
    print("📡 Client connected!")
    try:
        # Read up to 1KB of request
        request = await reader.read(1024)
        print("Request:", request)

        # Parse request
        request_str = request.decode()
        if "POST / " in request_str:
            # Extract form data
            body_split = request_str.split("\r\n\r\n", 1)
            if len(body_split) > 1:
                body = body_split[1]
                
                ssid = re.search(r'ssid=([^&]*)', body)
                password = re.search(r'password=([^&]*)', body)
                ssid_val = ssid.group(1) if ssid else ''
                password_val = password.group(1) if password else ''
                ssid_val = url_decode(ssid_val)
                password_val = url_decode(password_val)
                creds = {"ssid": ssid_val, "password": password_val}
                with open("wifi.json", "w") as f:
                    f.write(json.dumps(creds))
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "<h1>WiFi credentials saved! Rebooting...</h1>"
                )
                await writer.awrite(response)
                asyncio.create_task(delayed_reset())
            else:
                response = (
                    "HTTP/1.1 400 Bad Request\r\n"
                    "Content-Type: text/html\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "<h1>Bad Request</h1>"
                )
        else:
            # Read credentials from wifi.json
            
            ssid_val = ""
            password_val = ""
            try:
                with open("wifi.json", "r") as f:
                    creds = json.load(f)
                    ssid_val = creds.get("ssid", "")
                    password_val = creds.get("password", "")
            except Exception as e:
                print("Could not read wifi.json:", e)
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "Connection: close\r\n"
                "\r\n"
                "<h1>Setup Wifi</h1>"
                "<form method='POST'>"
                "SSID: <input name='ssid' type='text' value='" + ssid_val + "'><br>"
                "Password: <input name='password' type='password' value='" + password_val + "'><br>"
                "<input type='submit' value='Save'>"
                "</form>"
            )
        await writer.awrite(response)
        print("✅ Response sent")
    except Exception as e:
        print("❌ Error in handler:", e)
    finally:
        await writer.aclose()
        print("🔌 Client disconnected")

# ==== Web Server Start ====
async def start_web_server(ip):
    await asyncio.start_server(handle_client, ip, port=80)
    print(f"🌍 Server running at http://{ip}:80")
