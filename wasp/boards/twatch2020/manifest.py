# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Daniel Thompson

freeze('.', 'watch.py', opt=3)
freeze('../..',
    (
        'apps/clock.py',
        'apps/launcher.py'
        'apps/metronome.py',
        'apps/pager.py',
        'drivers/axp202c.py',
        'drivers/bma421.py',
        'drivers/st7789.py',
        'drivers/focaltouch.py',
        'drivers/pcf8563.py',
        'adapters/app.py',
        'adapters/backlight.py',
        'adapters/battery.py',
        'adapters/power_management_service.py',
        'adapters/rtc.py',
        'adapters/touch.py',
        'adapters/vibrator.py',
        'adapters/wifi.py',
        'fonts/__init__.py',
        'fonts/clock.py',
        'fonts/sans24.py',
        'fonts/sans28.py',
        'fonts/sans36.py',
        'boot.py',
        'draw565.py',
        'gadgetbridge.py',
        'icons.py',
        'ppg.py',
        'shell.py',
        'wasp.py',
        'widgets.py',
    ),
    opt=3
)
