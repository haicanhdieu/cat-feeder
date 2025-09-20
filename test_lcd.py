from ssd1306_display import SSD1306_I2C

display = SSD1306_I2C(width=128, height=64, scl_pin=1, sda_pin=0)
display.fill(0)
display.text("Hello OLED", 0, 0)
display.show()
