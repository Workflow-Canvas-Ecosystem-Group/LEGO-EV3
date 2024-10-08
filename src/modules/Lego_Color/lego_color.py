import logging
from ev3dev2.sensor.lego import ColorSensor
from utils import ADDRESS_MAP


class LegoColor:
    def __init__(self, device_info):
        self.color = ColorSensor(ADDRESS_MAP.get(device_info.get("port")))

    def get_color(self):
        return self.color.color_name

    def get_rgb(self):
        return list(self.color.rgb)

    def calibrate_white(self):
        return self.color.calibrate_white()
