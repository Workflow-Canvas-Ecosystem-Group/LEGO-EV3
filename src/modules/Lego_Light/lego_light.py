from ev3dev2.sensor.lego import LightSensor
from utils import ADDRESS_MAP


class LegoLight:
    def __init__(self, device_info):
        self.light = LightSensor(ADDRESS_MAP.get(device_info.get("port")))

    def reflected_light_intensity(self):
        return self.light.reflected_light_intensity()

    def ambient_light_intensity(self):
        return self.light.ambient_light_intensity()
