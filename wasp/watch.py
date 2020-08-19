from machine import I2C, SPI, Pin
import draw565
from drivers import axp202c as axp202
from drivers.focaltouch import FocalTouch
from drivers.st7789 import ST7789_SPI
from adapters.touch import Touch
from adapters.vibrator import Vibrator
from adapters.backlight import Backlight
from adapters.battery import Battery
from adapters.rtc import RTC


class Watch:

    def __init__(self, touch_callback = None):

        self.i2c0 = self.init_i2c0()
        self.i2c1 = self.init_i2c1()
        self.axp = self.init_axp(self.i2c0)
        self.backlight = Backlight(self.axp)
        self.vibrator = self.init_vibrator()
        self.ir = self.init_ir()
        self.display = self.init_display()
        self.drawable = draw565.Draw565(self.display)
        self.drawable.reset()
        self.drawable.string("booting", 10, 10)
        self.rtc = RTC(self.i2c0)
        self.touch = self._init_touch(self.i2c1, touch_callback)
        self.battery = Battery(self.axp)
        #self.accel = BMA421(self.i2c1)

    def init_i2c0(self):
        return I2C(0,scl=Pin(22), sda=Pin(21))

    def init_i2c1(self):
        return I2C(1,scl=Pin(32), sda=Pin(23))

    def init_axp(self, bus):
        axp = axp202.PMU(bus)
        axp.enablePower(axp202.AXP202_LDO2)
        axp.enablePower(axp202.AXP202_DCDC3)
        axp.clearIRQ()
        return axp

    def init_ir(self):
        ir = Pin(13, Pin.OUT)
        ir.off()
        return ir

    def init_vibrator(self):
        vibrator = Vibrator(Pin(4, Pin.OUT))
        return vibrator

    def init_display(self):
        spi = SPI(2, baudrate=32000000, polarity=1, phase=0, bits=8, firstbit=0, sck=Pin(18,Pin.OUT),mosi=Pin(19,Pin.OUT))
        spi.init()
        display = ST7789_SPI(240, 240, spi,
                             cs=Pin(5,Pin.OUT),dc=Pin(27,Pin.OUT))
        display.rotate(0)
        display.fill(0)
        return display

    def _init_touch(self, i2c, touch_callback):
        ft = FocalTouch(i2c)
        return Touch(ft, Pin(38, Pin.IN), touch_callback)
