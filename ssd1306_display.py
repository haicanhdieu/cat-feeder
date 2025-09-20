"""Driver for SSD1306 128x64/128x32 OLED displays over I2C."""

from micropython import const
import framebuf
from machine import I2C, Pin

SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

# SSD1306 columns are always 128 wide but shorter panels crop height
WIDTH_128 = const(128)
HEIGHT_64 = const(64)
HEIGHT_32 = const(32)


class SSD1306(framebuf.FrameBuffer):
    """Framebuffer backed driver that exposes drawing primitives."""

    def __init__(self, width, height, external_vcc=False):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        self.temp = bytearray(2)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        self.write_cmd(SET_DISP | 0x00)
        self.write_cmd(SET_MEM_ADDR)
        self.write_cmd(0x00)  # Horizontal addressing mode
        self.write_cmd(SET_DISP_START_LINE | 0x00)
        self.write_cmd(SET_SEG_REMAP | 0x01)
        self.write_cmd(SET_MUX_RATIO)
        self.write_cmd(self.height - 1)
        self.write_cmd(SET_COM_OUT_DIR | 0x08)
        self.write_cmd(SET_DISP_OFFSET)
        self.write_cmd(0x00)
        self.write_cmd(SET_COM_PIN_CFG)
        cfg = 0x12 if self.height == HEIGHT_64 else 0x02
        self.write_cmd(cfg)
        self.write_cmd(SET_DISP_CLK_DIV)
        self.write_cmd(0x80)
        self.write_cmd(SET_PRECHARGE)
        precharge = 0x22 if self.external_vcc else 0xF1
        self.write_cmd(precharge)
        self.write_cmd(SET_VCOM_DESEL)
        self.write_cmd(0x30)
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(0xFF)
        self.write_cmd(SET_ENTIRE_ON)
        self.write_cmd(SET_NORM_INV)
        self.write_cmd(SET_CHARGE_PUMP)
        charge = 0x10 if self.external_vcc else 0x14
        self.write_cmd(charge)
        self.write_cmd(SET_DISP | 0x01)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast & 0xFF)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (0x01 if invert else 0x00))

    def show(self):
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(0x00)
        self.write_cmd(self.width - 1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0x00)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)

    def write_cmd(self, cmd):  # pragma: no cover
        raise NotImplementedError

    def write_data(self, buf):  # pragma: no cover
        raise NotImplementedError


class SSD1306_I2C(SSD1306):
    """SSD1306 configured to communicate over I2C."""

    def __init__(self, width=WIDTH_128, height=HEIGHT_64, i2c=None, addr=0x3C, scl_pin=None, sda_pin=None, freq=400000, external_vcc=False):
        if i2c is None:
            if scl_pin is None or sda_pin is None:
                raise ValueError("Must supply I2C instance or SCL/SDA pin numbers")
            i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
        self.i2c = i2c
        self.addr = addr
        super().__init__(width, height, external_vcc=external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co = 1, D/C# = 0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        mv = memoryview(buf)
        for start in range(0, len(mv), 16):
            chunk = mv[start:start + 16]
            try:
                self.i2c.writevto(self.addr, (b'\x40', chunk))
            except AttributeError:
                self.i2c.writeto(self.addr, b'\x40' + bytes(chunk))
