import uasyncio as asyncio
import re

from scheduler import get_schedules, add_schedule, delete_schedule, FOOD_SIZES
from url_helper import url_decode
from string_helper import capitalize
import feeder

# ==== HTTP Handler ====
async def handle_client(reader, writer):
    print("📡 Client connected!")
    try:
        # Read up to 1KB of request
        request = await reader.read(1024)
        print("Request:", request)

        request_str = request.decode()
        method = "GET"
        if request_str.startswith("POST"):
            method = "POST"

        # Handle form submission
        if method == "POST":
            body_split = request_str.split("\r\n\r\n", 1)
            if len(body_split) > 1:
                body = body_split[1]

                # Parse form data
                def get_val(key):
                    m = re.search(key + r'=([^&]*)', body)
                    return m.group(1) if m else ""

                action = get_val("action")
                time_str = get_val("time")
                size = get_val("size")
                time_str = url_decode(time_str)
                size = url_decode(size)

                if action == "add" and time_str and size:
                    print("Adding schedule:", time_str, size)
                    add_schedule(time_str, size)
                elif action == "delete" and time_str:
                    print("Deleting schedule:", time_str)
                    delete_schedule(time_str)
                elif action == "feed_now":
                    print("Feeding now - 3 turns")
                    asyncio.create_task(feeder.feed(3))

        # Render scheduler table and form
        schedules = get_schedules()
        print("Current schedules:", schedules)

        html = "<h1>Pet Feeder Scheduler</h1>"
        # Control Section (moved to top)
        html += "<div style='border:1px solid #ccc; padding:16px; margin-bottom:24px;'>"
        html += "<h2>Control</h2>"
        html += "<form method='POST'>"
        html += "<input type='hidden' name='action' value='feed_now'>"
        html += "<button type='submit' style='font-size:1.2em; padding:10px 24px; background:#28a745; color:white; border:none; border-radius:8px; cursor:pointer;'>Feed Now</button>"
        html += "</form>"
        html += "</div>"

        # Schedules Section
        html += "<div style='border:1px solid #ccc; padding:16px;'>"
        html += "<h2>Schedules</h2>"
        html += "<form method='POST' style='margin-bottom:16px;'>"
        html += "Time (HH:MM): <input name='time' type='time'> "
        html += "Size: <select name='size'>"
        for sz in FOOD_SIZES:
            html += "<option value='" + str(sz) + "'>" + capitalize(str(sz)) + "</option>"
        html += "</select> "
        html += "<input type='hidden' name='action' value='add'>"
        html += "<input type='submit' value='Add'>"
        html += "</form>"

        html += "<table style='width:100%; border-collapse:collapse;'>"
        html += "<tr>"
        html += "<th style='text-align:left; padding:8px 16px;'>Time</th>"
        html += "<th style='text-align:left; padding:8px 16px; width:120px;'>Size</th>"
        html += "<th style='text-align:left; padding:8px 16px; width:120px;'>Action</th>"
        html += "</tr>"
        for t, sz in schedules.items():
            html += "<tr>"
            html += "<td style='padding:8px 16px;'>" + str(t) + "</td>"
            html += "<td style='padding:8px 16px; width:120px;'>" + capitalize(str(sz)) + "</td>"
            html += "<td style='padding:8px 16px; width:120px;'>"
            html += "<form method='POST' style='display:inline'>"
            html += "<input type='hidden' name='time' value='" + str(t) + "'>"
            html += "<input type='hidden' name='action' value='delete'>"
            html += "<input type='submit' value='Delete'>"
            html += "</form>"
            html += "</td>"
            html += "</tr>"
        html += "</table>"
        html += "</div>"

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Connection: close\r\n"
            "\r\n"
            + html
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
    await asyncio.start_server(handle_client, ip, 80)
    print(f"🌍 Server running at http://{ip}")
