from button import Button
import uasyncio as asyncio
import feeder


def feed():
    print("Feeding...")
    asyncio.create_task(feeder.feed(3))

button = Button(pin=6, callback=feed)  # Replace 17 with your GPIO pin number
async def monitor_button():
    await button.monitor_button()
    # pass
