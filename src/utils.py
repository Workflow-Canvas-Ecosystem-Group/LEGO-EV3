from ev3dev2._platform.ev3 import *


ADDRESS_MAP = {
    "1": INPUT_1,
    "2": INPUT_2,
    "3": INPUT_3,
    "4": INPUT_4,

    "A": OUTPUT_A,
    "B": OUTPUT_B,
    "C": OUTPUT_C,
    "D": OUTPUT_D,

}


class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


# limit vlue to [min_value, max_value]
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))
