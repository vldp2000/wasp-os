# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Daniel Thompson

"""Metronome
~~~~~~~~~~~~~

Produce the motor vibration using the specified tempo
"""

import wasp
import icons
import time
import logging


class MetronomeApp(object):
    """Metronome application."""
    NAME = 'Metronome'
    ICON = icons.bomb

    def __init__(self, play = False, tempo = 120, beats_per_measure = 4, number_of_measures = 4, accent = False):
        self.play = play
        self.tempo = tempo
        self.beats_per_measure = beats_per_measure
        self.number_of_measures = number_of_measures
        self.accent = accent
        self.delay = int((60 * 1000 / tempo))
        self.current_bit = '0..0'
        self.bitGenerator = self.get_next_bit()
        self.last_tick = time.ticks_ms()
        
        self.log = logging.getLogger('wasp')


    def touch(self, event):
        """Notify the application of a touchscreen touch event."""
        self.play = False

    def foreground(self):
        """Activate the application."""
        self.draw()
        wasp.system.request_tick(int(self.delay/2))
        self.play = True

    def background(self):
        """De-activate the application (without losing state)."""
        self.play = False

    def tick(self, ticks):
        wasp.system.keep_awake()
        if self.play:
            
            self.log.debug( 'last tick {}'.format(self.last_tick))

            nextBit = next(self.bitGenerator)
            self.current_bit = '{}..{}'.format(nextBit[0],nextBit[1])
            wasp.system.watch.vibrator.pulse(25,5)
            self.draw()
            
            if self.last_tick > 0:
                delayDelta = time.ticks_diff(time.ticks_ms(), self.last_tick)
                self.log.debug('delay ={}'.format(self.delay)) 
                self.log.debug('delta ={}'.format(delayDelta))
                self.log.debug('extra = {}'.format(self.delay - delayDelta))
                if delayDelta < self.delay:
                    time.sleep_ms(self.delay -  delayDelta)

            self.last_tick = time.ticks_ms()
            self.log.debug( 'last tick {}'.format(self.last_tick))
            self.log.debug('-------')

    def draw(self):
        """Redraw the display from scratch."""
        draw = wasp.system.watch.drawable
        draw.fill()
        draw.string('T.{} S.{}/{}'.format(self.tempo, self.beats_per_measure, self.number_of_measures), 2, 60, width=240)        
        draw.string('Bit {}'.format(self.current_bit), 10, 108, width=240)        

    def get_next_bit(self):
        while self.play:
            for m in range(1, self.number_of_measures + 1):
                for b in range(1, self.beats_per_measure + 1):
                    yield (b,m)
