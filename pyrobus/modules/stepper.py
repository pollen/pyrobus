from __future__ import division

import time

from .module import Module, interact


class Stepper(Module):
    def __init__(self, id, alias, robot):
        Module.__init__(self, 'Stepper', id, alias, robot)

        # Read
        self._position = None

        # Write
        self._target_position = None
        self._target_speed = None
        self._home = 0

    @property
    def position(self):
        """ Current position in steps """
        return self._position

    @property
    def is_moving(self):
        """ Is the stepper moving """
        return self._position != self._target_position

    def wait_until_idle(self):
        while self.is_moving:
            time.sleep(0.1)

    @property
    def target_position(self):
        """ Target position in steps. """
        return self._target_position

    @target_position.setter
    def target_position(self, new_pos):
        if new_pos != self._target_position:
            self._target_position = new_pos
            self._push_value('target_position', self._target_position)

    @property
    def target_speed(self):
        """ Speed in step per seconds. """
        return self._target_speed

    @target_speed.setter
    def target_speed(self, new_speed):
        if new_speed != self._target_speed:
            self._target_speed = new_speed
            self._push_value('target_speed', self._target_speed)

    def home(self):
        self._push_value('home', self._home)
        self._home = 1 - self._home

    def _update(self, new_state):
        new_pos = new_state['position']
        # self._is_moving = new_state['is_moving']

        if new_pos != self._position:
            self._pub_event('moved', self._position, new_pos)
            self._position = new_pos