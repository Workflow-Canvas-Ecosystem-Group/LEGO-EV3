import logging
from ev3dev2.sensor.lego import TouchSensor
from utils import ADDRESS_MAP


class LegoTouch:
    def __init__(self, device_info):
        self.touch = TouchSensor(ADDRESS_MAP.get(device_info.get("port")))

    def is_pressed(self):
        """
        A boolean indicating whether the current touch sensor is being
        pressed.
        """

        return self.touch.is_pressed

    def is_released(self):
        return self.touch.is_released

    def wait_for_pressed(self, timeout_ms=None):
        return self.touch.wait_for_pressed(timeout_ms)

    def wait_for_released(self, timeout_ms=None):
        return self.touch.wait_for_released(timeout_ms)

    def wait_for_bump(self, timeout_ms=None):
        """
        Wait for the touch sensor to be pressed down and then released.
        Both actions must happen within timeout_ms.
        """
        return self.touch.wait_for_bump(timeout_ms)
