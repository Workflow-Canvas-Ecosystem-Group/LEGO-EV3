import logging
from ev3dev2.sound import Sound
from utils import clamp


class LegoSound:
    def __init__(self, device_info):
        self.sound = Sound()

    def beep(self, volume=100, block=True):
        self.sound.set_volume(clamp(volume, 1, 100))
        self.sound.beep(play_type=Sound.PLAY_WAIT_FOR_COMPLETE if block else Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    def speak(self, text, volume=100, speed=50, block=True):
        opts = "-a 200 -s {}".format(int(float(speed) / 100.0 * 150))
        return self.sound.speak(text=text, volume=clamp(volume, 1, 100), espeak_opts=opts, play_type=Sound.PLAY_WAIT_FOR_COMPLETE if block else Sound.PLAY_NO_WAIT_FOR_COMPLETE)
