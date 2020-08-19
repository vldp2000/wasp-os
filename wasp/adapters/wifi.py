import json
import uasyncio as asyncio
import network


class Wifi:

    def __init__(self):
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(False)

    def sleep(self):
        self.wifi.active(False)

    async def wake(self):
        self.wifi.active(True)
        await asyncio.sleep(0)
        network = self._search_network()
        await asyncio.sleep(0)
        if network is None:
            print("sin wifis conectables")
            return False
        await asyncio.sleep(0)
        print(network[0], network[1])
        await self._try_wlan_connect(network[0], network[1])
        if self.wifi.isconnected():
            return True
        return False

    def isconnected(self):
        return self.wifi.isconnected()

    def _search_network(self):
        my_networks = self._my_networks()
        networks = self.wifi.scan()
        for network in networks:
            if network[0].decode() in my_networks:
                return network[0].decode(), my_networks[network[0].decode()]
        return None

    def _my_networks(self):
        with open('/fs/wifi.json', 'r') as f:
            data = json.loads(f.read())
            f.close()
        return data

    async def _try_wlan_connect(self, ssid, password):
        await asyncio.sleep(0)
        self.wifi.connect(ssid, password)
        for _ in range(60):
            if self.wifi.status() != network.STAT_CONNECTING:
                break
            await asyncio.sleep(1)

        if self.wifi.status() == network.STAT_CONNECTING:
            self.wifi.disconnect()
            await asyncio.sleep(1)
