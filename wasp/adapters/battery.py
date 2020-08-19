

class Battery():

    def __init__(self, axp202):
        self._driver = axp202

    def charging(self):
        return self._driver.isChargeing() > 0

    def power(self):
        return self._driver.isVBUSPlug() > 0

    def voltage_mv(self):
        return self._driver.getBattVoltage()

    def level(self):
        return self._driver.getBattPercentage()
