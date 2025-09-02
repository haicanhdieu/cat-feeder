from machine import Pin
import uasyncio as asyncio

class Button:
    def __init__(self, pin, callback=None):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.callback = callback

    async def monitor_button(self):
        try:
            while True:
                if not self.pin.value():  # Button is pressed (active low)
                    print("Button pressed!")
                    if self.callback:
                        self.callback()  # Execute the callback function
                    await asyncio.sleep(0.5)  # Debounce delay
                await asyncio.sleep(0.1)  # Polling delay
        except KeyboardInterrupt:
            print("Exiting button monitoring.")

