import logging
from ev3dev2.sensor.lego import UltrasonicSensor
from utils import ADDRESS_MAP


class LegoUltrasonic:
    def __init__(self, device_info):
        self.us = UltrasonicSensor(ADDRESS_MAP.get(device_info.get("port")))

    def start(self):
        self.us.distance_centimeters_continuous

    def stop(self):
        self.us.distance_centimeters_ping

    def get_distance(self):
        return self.us.distance_centimeters
