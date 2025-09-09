import uasyncio as asyncio
from i2c_lcd import I2cLcd

class Lcd:
    def __init__(self, scl_pin=1, sda_pin=0):
        # Create LCD instance
        self.lcd = I2cLcd(scl_pin=1, sda_pin=0, i2c_addr=0x27, num_lines=2, num_columns=16)

    async def write(self, message, clear=True):
        if clear:
            self.lcd.clear()
        await asyncio.sleep(0.1)
        self.lcd.putstr(message)
        
    async def clear_line(self, line):
        if line < 0 or line >= self.lcd.num_lines:
            raise ValueError("Line number out of range")
        self.lcd.move_to(0, line)
        self.lcd.putstr(" " * self.lcd.num_columns)
        
    async def write_line(self, message, line = 0):
        if line < 0 or line >= self.lcd.num_lines:
            raise ValueError("Line number out of range")
        self.lcd.move_to(0, line)
        self.clear_line(line)
        await asyncio.sleep(0.1)
        self.lcd.move_to(0, line)
        self.lcd.putstr(message)
        await asyncio.sleep(0.1)

    async def clear(self):
        self.lcd.clear()
        await asyncio.sleep(0.1)

    async def backlight_on(self):
        self.lcd.hal_backlight_on()
        await asyncio.sleep(0.1)

    async def backlight_off(self):
        self.lcd.hal_backlight_off()
        await asyncio.sleep(0)
