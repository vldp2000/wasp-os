
from machine import Pin

BACKLIGHT_LOW = 2600
BACKLIGHT_MEDIUM = 2950
BACKLIGHT_HIGHT = 3300


class Backlight():

    bl = Pin(12, Pin.OUT)

    def __init__(self, axp, level=BACKLIGHT_MEDIUM):
        self.axp = axp
        self.set(level)

    def set(self, level):
        if level == 0:
            self.bl.off()
        else:
            self.bl.on()
            if level == 1:
                self.axp.setLDO2Voltage(BACKLIGHT_LOW)
            elif level == 2:
                self.axp.setLDO2Voltage(BACKLIGHT_MEDIUM)
            elif level == 3:
                self.axp.setLDO2Voltage(BACKLIGHT_HIGHT)