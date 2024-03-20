import sys
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# how far back from the end to replace a space with a newline
newline_range = 5

# compatible with all versions of RPI as of Jan. 2019
# v1 - v3B+
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)


# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

print("Starting LCD printing")
try:
    for raw_in in sys.stdin:
        stripped = raw_in.strip()
        if not stripped:
            break
        if stripped.lower() in ['quit', 'q']:
            break
        text = list(stripped)
        formatted = []
        for i in range(lcd_rows):
            if len(text) > lcd_columns:
                space_found = False
                # check newline_range characters back for a space and separate
                start = lcd_columns - newline_range
                for index in range(start, lcd_columns):
                    if text[index] == ' ':
                        space_found = True
                        # if a space is found, do a newline, continue lcd rows
                        text[index] = '\n'
                        formatted += text[:(index+1)]
                        text = text[(index+1):]
                        break
                # if a space is not found, separate back one, insert a dash
                if not space_found:
                    # strip off space or newline characters at the end of rows
                    if text[lcd_columns] == ' ':
                        text[lcd_columns] = '\n'
                    else:
                        text.insert(lcd_columns-1, '-\n')
                    formatted += text[:lcd_columns]
                    text = text[lcd_columns:]
            else:
                formatted += text
                break
            

        lcd.clear()
        lcd.message = "".join(formatted)

except KeyboardInterrupt:
    print("\n")

print("Stopping LCD")
lcd.clear()

