import time
import threading

import board
import adafruit_lis3mdl

'''
Everything here is in units of seconds and turns. Let the display deal with tracking distance.
'''

class Sensor(threading.Thread):
    def __init__(self):
        super().__init__()

        i2c = board.I2C()
        self.sensor = adafruit_lis3mdl.LIS3MDL(i2c)

        self.data_rate = adafruit_lis3mdl.Rate.string[self.sensor.data_rate]
        self.sampling_period = 1 / self.data_rate

        self.mag_near_threshold = 60 # microtesla
        self.mag_far_threshold = 35

        self.exit_event = threading.Event()

        self.dist = 0
        self.speed = 0

    def exit(self):
        self.exit_event.set()

    def mag_near(self):
        return abs(self.sensor.magnetic[2]) > self.mag_near_threshold

    def mag_far(self):
        return abs(self.sensor.magnetic[2]) < self.mag_far_threshold

    def run(self):
        # average speed over one second
        timer = time.perf_counter()
        toggle = self.mag_near()
        dist = 0
        while not self.exit_event.is_set():
            time.sleep(self.sampling_period)
            if toggle and self.mag_far():
                # count a pass, 
                toggle = False
                dist += 1
            elif self.mag_near():
                # reset the toggle
                toggle = True
            elif time.perf_counter() - timer > 1:
                self.speed = dist
                self.dist += dist
                dist = 0
                timer = time.perf_counter()

            
