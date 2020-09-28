import time

from drivers.pcf8563 import PCF8563


class RTC(object):

    def __init__(self, i2c):
        self._rtc = PCF8563(i2c)
        self._tick_init = time.ticks_ms()

    def set_localtime(self, t):
        """Set the current wall time.

        :param sequence t:
                Wall time formatted as (yyyy, mm, dd, HH, MM, SS, DOW), any
                additional elements in sequence will be ignored.
        """


        yyyy = t[0]
        mm = t[1]
        dd = t[2]
        HH = t[3]+10
        if HH>23:
            HH = 0+(HH-24)
        MM = t[4]
        SS = t[5]

        t = (yyyy, mm, dd, HH, MM, SS, 2)

        self._rtc.set_datetime(t)

    def sync_time(self):
        try:
            import ntptime
            ntptime.settime()
            import time
            t = time.localtime()
            self.set_localtime(t)
        except:
            pass

    def get_localtime(self):
        """Get the current time and date.

        :returns: Wall time formatted as (yyyy, mm, dd, wday, HH, MM, SS)
        """
        return (self._rtc.year(), self._rtc.month(), self._rtc.day(),
                self._rtc.hours(), self._rtc.minutes(),
                self._rtc.seconds(), self._rtc.day_of_week())

    def get_time(self):
        """Get the current time.

        :returns: Wall time formatted as (HH, MM, SS)
        """
        localtime = self.get_localtime()
        return localtime[3:6]

    @property
    def uptime(self):
        """Provide the current uptime in seconds."""
        return int(time.ticks_ms()/1000)

    def get_uptime_ms(self):
        """Return the current uptime in milliseconds."""
        return time.ticks_ms()
