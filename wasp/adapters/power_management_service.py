import uasyncio as asyncio
import machine
import drivers.axp202c as axp202
from aswitch import Delay_ms
from wasp import system as wasp
from machine import Pin
import esp32
import logging


class PMS:
    def __init__(self, blank_after_s):
        self.wasp = wasp
        self.log = logging.getLogger("pms")
        self._keep_awake_timer = None
        self._awake_time = blank_after_s * 1000
        self.installirqhandler()
        self._keep_awake_event = asyncio.Event()
        self._keep_awake_event.set()
        self.last_connection = 0

    def init(self):
        asyncio.create_task(self.loop())

    async def loop(self):
        await asyncio.sleep(15)
        while True:
            self.log.debug("loop")
            try:
                await self._keep_awake_event.wait()
                self.wasp.sleep()
                machine.lightsleep(300000)
                reason = machine.wake_reason()
                self.log.debug("wake reason:" + str(reason))
                if reason == 2:
                    await self.wasp.wake(by_user=True)
                    self.keep_awake()
                elif reason == 4:
                    await self.wasp.wake(by_user=False)
                    self.keep_awake(True, 15000)
            except Exception as e:
                self.log.exc(e, "loop")



    def keep_awake(self, value=True, time=None):
        awake_time = self._awake_time
        if time:
            awake_time = time
        self.log.debug("keep_awake: "+str(value))
        if value:
            if self._keep_awake_timer is None:
                self._keep_awake_timer = Delay_ms(self._sleep)
                self._keep_awake_timer.trigger(awake_time)
            else:
                self._keep_awake_timer.stop()
                self._keep_awake_timer = Delay_ms(self._sleep)
                self._keep_awake_timer.trigger(awake_time)
            self._keep_awake_event.clear()
        else:
            if self._keep_awake_timer:
                self._keep_awake_timer.stop()
                self._keep_awake_timer = None
            self._keep_awake_event.set()

    def _sleep(self):
        self.log.debug("_sleep")
        self.keep_awake(False)

    def installirqhandler(self):
        # define the irq handlers within this method so we have
        # access to self (closure) without global variable
        self.axp = self.wasp.watch.axp
        self.axp.enableIRQ(axp202.AXP202_PEK_SHORTPRESS_IRQ)
        #self.axp.enableIRQ(axp202.AXP202_CHARGING_IRQ)
        #self.axp.enableIRQ(axp202.AXP202_CHIP_TEMP_HIGH_IRQ)
        #self.axp.enableIRQ(axp202.AXP202_BATT_OVER_TEMP_IRQ)
        #self.axp.enableIRQ(axp202.AXP202_CHARGING_FINISHED_IRQ)
        #self.axp.enableIRQ(axp202.AXP202_CHARGING_IRQ)
        #self.axp.enableIRQ(axp202.AXP202_BATT_EXIT_ACTIVATE_IRQ)
        #self.axp.enableIRQ(axp202.AXP202_BATT_ACTIVATE_IRQ)

        def axp_interrupt(pin):
            irq = self.axp.readIRQ()
            self.log.debug("axp interrupt: " + str(irq))
            try:
                if 0x20000 in irq:
                    self.wasp.handle_button(1)
                else:
                    self.log.debug("axp irq unknow" + str(irq))
            except:
                pass
            self.axp.clearIRQ()

        def rtc_interrupt(pin):
            self.log.debug("Got RTC Interrupt on pin:", pin)

        def bma_interrupt(pin):
            self.log.debug("bma interrupt" + str(pin))
            self.log.debug("Got BMA Accellorator Interrupt on pin:", pin)

        self.rtcint = Pin(37, Pin.IN)
        self.rtcint.irq(trigger=Pin.IRQ_FALLING, handler=rtc_interrupt)
        self.axpint = Pin(35, Pin.IN)
        self.axpint.irq(trigger=Pin.IRQ_FALLING, handler=axp_interrupt)
        self.bmaint = Pin(39, Pin.IN)
        self.bmaint.irq(trigger=Pin.IRQ_RISING, handler=bma_interrupt)
        esp32.wake_on_ext0(self.axpint, esp32.WAKEUP_ALL_LOW)
