import machine
import uasyncio as asyncio

# Define a constant for the LED pin
LED_PIN = "LED"

# Define a helper function to get the LED pin
def get_led():
    return machine.Pin(LED_PIN, machine.Pin.OUT)

# ==== LED Blink Modes ====
async def blink_led(interval=1):
    """Blink forever while server is running"""
    led = get_led()
    while True:
        led.on()
        await asyncio.sleep(interval)
        led.off()
        await asyncio.sleep(interval)

# Define a function to turn off the LED
def turn_off_led():
    led = get_led()
    led.off()

# Define a function to turn on the LED
def turn_on_led():
    led = get_led()
    led.on()

# Define a function to blink the LED fast
async def blink_led_fast(interval=0.2):
    """Blink the LED quickly while the server is running"""
    await blink_led(interval)

# Define a function to blink the LED slowly
async def blink_led_slow(interval=1):
    """Blink the LED slowly while the server is running"""
    await blink_led(interval)
