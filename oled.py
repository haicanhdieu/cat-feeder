import uasyncio as asyncio
from ssd1306_display import SSD1306_I2C


class Oled:
    def __init__(self, *, width=128, height=64, scl_pin=1, sda_pin=0, addr=0x3C, freq=400000, i2c=None, line_height=8, char_width=8):
        self.display = SSD1306_I2C(width=width, height=height, i2c=i2c, addr=addr, scl_pin=scl_pin, sda_pin=sda_pin, freq=freq)
        self.line_height = line_height
        self.char_width = char_width
        self.num_lines = self.display.height // self.line_height
        self.num_columns = self.display.width // self.char_width

    async def write(self, message, clear=True):
        if clear:
            self.display.fill(0)
        lines = message.split("\n")
        for idx, text in enumerate(lines):
            if idx >= self.num_lines:
                break
            self._render_line(text, idx, clear_line=not clear, update=False)
        self.display.show()
        await asyncio.sleep(0)

    async def clear_line(self, line):
        self._assert_line(line)
        self._clear_line_area(line)
        self.display.show()
        await asyncio.sleep(0)

    async def write_line(self, message, line=0):
        self._assert_line(line)
        self._render_line(message, line)
        await asyncio.sleep(0)

    async def clear(self):
        self.display.fill(0)
        self.display.show()
        await asyncio.sleep(0)

    async def power_on(self):
        self.display.poweron()
        await asyncio.sleep(0)

    async def power_off(self):
        self.display.poweroff()
        await asyncio.sleep(0)

    async def invert(self, enable=True):
        self.display.invert(bool(enable))
        await asyncio.sleep(0)

    async def set_contrast(self, value):
        self.display.contrast(value)
        await asyncio.sleep(0)

    def _assert_line(self, line):
        if line < 0 or line >= self.num_lines:
            raise ValueError("Line number out of range")

    def _clear_line_area(self, line):
        y = line * self.line_height
        self.display.fill_rect(0, y, self.display.width, self.line_height, 0)

    def _render_line(self, message, line, *, clear_line=True, update=True):
        if clear_line:
            self._clear_line_area(line)
        y = line * self.line_height
        text = message[:self.num_columns]
        self.display.text(text, 0, y)
        if update:
            self.display.show()
