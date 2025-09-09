from lcd import Lcd

lcd = Lcd()

async def lcd_write(message):
    await lcd.write(message)
    
async def lcd_write_line(message, line=0):
    await lcd.write_line(message, line)
    
async def lcd_clear():
    await lcd.clear()
    

    