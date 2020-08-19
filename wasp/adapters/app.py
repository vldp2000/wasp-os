import uasyncio as asyncio
import sys


class App:

    def __init__(self, app):
        self._fg_period = 1000
        self._task = None
        self._in_foreground = asyncio.Event()
        self._app = app
        self.NAME = app.NAME
        self.ICON = app.ICON
        if 'tick' in dir(app):
            self._task = asyncio.create_task(self.loop())

    async def loop(self):
        try:
            while True:
                try:
                    if self._in_foreground.is_set():
                        self._app.tick(0)
                    else:
                        if 'tick_background' in dir(self._app):
                            self._app.tick_background(0)
                        else:
                            await self._in_foreground.wait()
                            continue
                except Exception as e:
                    sys.print_exception(e)
                await asyncio.sleep_ms(self._fg_period)
        except Exception as e:
            sys.print_exception(e)

    def foreground(self):
        if not self._in_foreground.is_set():
            self._in_foreground.set()
            self._app.foreground()

    def background(self):
        if self._in_foreground.is_set():
            self._in_foreground.clear()
            if 'background' in dir(self._app):
                self._app.background()

    def touch(self, event):
        if 'touch' in dir(self._app):
            self._app.touch(event)

    def swipe(self, event):
        if 'swipe' in dir(self._app):
            self._app.swipe(event)

    def press(self, button, state):
        if 'press' in dir(self._app):
            self._app.press(button, state)
