from oled import Oled

oled = Oled()

async def oled_write(message, clear=True):
    await oled.write(message, clear=clear)

async def oled_write_line(message, line=0):
    await oled.write_line(message, line=line)

async def oled_clear():
    await oled.clear()

async def oled_clear_line(line):
    await oled.clear_line(line)

async def oled_power_on():
    await oled.power_on()

async def oled_power_off():
    await oled.power_off()

async def oled_invert(enable=True):
    await oled.invert(enable)

async def oled_set_contrast(value):
    await oled.set_contrast(value)
