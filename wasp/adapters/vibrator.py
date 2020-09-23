import time
from machine import PWM


class Vibrator(object):
    def __init__(self, pin, active_low=False):

        pin.value(active_low)
        self.pin = pin
        self.freq = 10000
        self.active_low = active_low

    def pulse(self, duty=25, ms=40):

        pwm = PWM(self.pin, freq=self.freq, duty=duty)
        pwm.init()
        time.sleep_ms(ms)
        pwm.deinit()
        self.pin.value(self.active_low)
