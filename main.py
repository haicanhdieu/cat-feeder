import uasyncio as asyncio
from led import blink_led_fast, blink_led_slow, turn_on_led, turn_off_led
from wifi import connect_wifi
from scheduler_webserver import start_web_server
from ap_webserver import start_web_server as start_ap_web_server
from button_controller import monitor_button
from scheduler_job import run_scheduled_jobs
from lcd_controller import lcd_write, lcd_write_line, lcd_clear
from feeder import stop



# Global variable for IP address
ip = None

# ==== Connect to WiFi ====
async def connect_to_wifi():
    """
    Handles the WiFi connection logic, including blinking LED during connection.
    """
    # Blink LED fast while connecting to WiFi
    blink_task = asyncio.create_task(blink_led_fast())
    try:
        wlan = await connect_wifi()
    except Exception as e:
        print(f"Error during WiFi connection: {e}")
        return None
    finally:
        blink_task.cancel()
        await asyncio.sleep(0)  # Allow the cancellation to propagate

    # Turn on LED after successful connection
    turn_on_led()
    return wlan

async def start_ap_mode():
    """
    Starts the Access Point (AP) mode.
    """
    from ap import enable_ap_mode

    print("Starting Access Point mode...")
    ap = await enable_ap_mode()
    print("Access Point mode is now active.")
    return ap

# ==== Main App ====
async def main():
    global ip  # Declare ip as global to modify it
    
    await stop()  # Ensure motor is stopped on startup
    
    await lcd_write("Connecting to WiFi...")
    wlan = await connect_to_wifi()
    
    # if wlan is not None
    if wlan is None:
        print("Start ap mode for wifi setup")
        ap = await start_ap_mode()
        # slow blink led
        asyncio.create_task(blink_led_slow())
        # Start AP web server
        ip = ap.ifconfig()[0]
        await start_ap_web_server(ip)
    else:
        # Start web server
        await lcd_write("Starting webserver...")
        ip = wlan.ifconfig()[0]
        await start_web_server(ip)
        

    # Start button monitoring
    asyncio.create_task(monitor_button())

    # Start scheduler job
    asyncio.create_task(run_scheduled_jobs())
    await lcd_clear()
    await lcd_write_line(ip, 0)
    await lcd_write_line("READY", 1)

    # Keep loop alive forever
    while True:
        await asyncio.sleep(3600)
        

# ==== Run ====
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("🛑 Application stopped")
finally:
    turn_off_led()
    print("LED turned off")
