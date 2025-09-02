# ap.py

import network
import uasyncio as asyncio

# Define constants for AP configuration
AP_SSID = 'PicoW_AP'
AP_PASSWORD = '12345678'
AP_CHANNEL = 1

async def enable_ap_mode(ssid=AP_SSID, password=AP_PASSWORD, channel=AP_CHANNEL):
    """
    Enable Access Point (AP) mode on the device.

    :param ssid: The SSID of the access point.
    :param password: The password for the access point.
    :param channel: The WiFi channel for the access point.
    """
    ap = network.WLAN(network.AP_IF)
    try:
        ap.active(False)  # Reset AP
        await asyncio.sleep(1)
        ap.config(essid=ssid, password=password, channel=channel)
        ap.active(True)
        await asyncio.sleep(3)  # Wait for initialization

        print('AP Mode Active')
        print('IP Address:', ap.ifconfig()[0])  # Should be 192.168.4.1
        print('AP Status:', ap.status())  # Should be 3
        print('AP Config:', ap.config('essid'), ap.config('channel'))

        return ap

    except Exception as e:
        print(f'AP Config Error (Channel {channel}):', e)
        ap.active(False)
        return None
