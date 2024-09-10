import sys
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from itertools import chain

from time import struct_time, strftime

class BikeLCD(characterlcd.Character_LCD_Mono):
    # Modify this if you have a different sized character LCD
    columns = 16
    lines = 2

    # how far back from the end to replace a space with a newline
    newline_range = 5

    pinout = {
        'rs': board.D17,
        'en': board.D27,
        'db4': board.D22,
        'db5': board.D23,
        'db6': board.D24,
        'db7': board.D25
    }
    pinout = {key: digitalio.DigitalInOut(pin) for key, pin in pinout.items()}

    _layout = [
            ['dist', 'time'],
            ['speed', 'avg_speed']
    ]

    lengths = {
            'time': len('HH:MM:SS'),
            'dist': len('000.0mi'),
            'speed': len('00.0mph'),
            'avg_speed': len('00.0mph')
    }

    settings = {
            'time': {'format':'%H:%M:%S'},
            'dist': {'units':'mi'},
            'speed': {'units':'mph'},
            'avg_speed': {'units':'mph'}
    }



    def __init__(self, *args, **kwargs):
        # Initialise the lcd class
        if args or kwargs:
            super().__init__(*args, **kwargs)
            self.pinout = {
                'rs':self.reset,
                'en':self.enbable,
                'db4':self.dl4,
                'db5':self.dl5,
                'db6':self.dl6,
                'db7':self.dl7
            }
                 
        else:
            super().__init__(columns=self.columns, lines=self.lines, **self.pinout)

        # get all the row/column info sorted out through the layout property
        self._coords = {}
        self.layout = self._layout

        self._time = None
        self._dist = None
        self._speed = None
        self._avg_speed = None

    @property
    def layout(self) -> list:
        return self._layout

    @layout.setter
    def layout(self, layout: list):
        self.clear()
        self._layout = layout
        for i, row in enumerate(layout):
            for j, val in enumerate(row):
                # right or left align based on position in list
                # if I get a bigger display or want centering logic I'll need to change this
                self._coords[val] = (j*(self.columns - self.lengths[val]), i)

    def write(self, string):
        self.cursor_position(self.column, self.row)
        for character in string:
            self._write8(ord(character), True)

        self.column, self.row = 0, 0

    @property
    def time(self) -> str:
        """Set the area of the lcd allocated for time"""
        return self._time


    @time.setter
    def time(self, time: struct_time):
        if 'time' not in self._coords:
            print("Time not in layout")
            return
        time = strftime('%H:%M:%S', time)
        if len(time) != self.lengths['time']:
            print(f"Invalid time format: {time}")
            return
        self._time = time

        self.column, self.row = self._coords['time']
        self.write(time)


    @property
    def dist(self) -> str:
        return self._dist

    @dist.setter
    def dist(self, dist: float):
        self._dist = '{:0=5.1f}{}'.format(dist, self.settings['dist']['units'])
        self.column, self.row = self._coords['dist']
        self.write(self._dist)


    @property
    def speed(self) -> str:
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = '{:0=4.1f}{}'.format(speed, self.settings['speed']['units'])
        self.column, self.row = self._coords['speed']
        self.write(self._speed)

    @property
    def avg_speed(self) -> str:
        return self._avg_speed

    @avg_speed.setter
    def avg_speed(self, avg_speed: float):
        self._avg_speed = '{:0=4.1f}{}'.format(avg_speed, self.settings['avg_speed']['units'])
        self.column, self.row = self._coords['avg_speed']
        self.write(self._avg_speed)


if __name__ == "__main__":
    print("Testing Display")

    from time import localtime, sleep

    lcd = BikeLCD()

    def test_speed(lcd):
        print("Speed Display")
        lcd.speed = 1.00134
        sleep(2)
        lcd.speed = 12.56423
        sleep(2)
        lcd.speed = 0.06

    def test_avg_speed(lcd):
        print("Speed Display")
        lcd.avg_speed = 1.00134
        sleep(2)
        lcd.avg_speed = 12.56423
        sleep(2)
        lcd.avg_speed = 0.06

    def test_dist(lcd):
        print("Distance Display")
        lcd.dist = 123.5
        sleep(2)
        lcd.dist = 12.1
        sleep(2)
        lcd.dist = 1.0004
        sleep(2)

    def test_time(lcd):
        print("Time Display")
        i = 0
        while i < 5:
            lcd.time = localtime()
            sleep(1)
            i += 1

    test_dist(lcd)

    test_speed(lcd)
    test_avg_speed(lcd)

    test_time(lcd)
    lcd.layout = [
            ['time', 'avg_speed'],
            ['speed', 'dist']
    ]

    test_time(lcd)


    
    print("Done.")
