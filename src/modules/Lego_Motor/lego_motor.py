from ev3dev2.motor import LargeMotor, MediumMotor
from utils import ADDRESS_MAP, clamp


class LegoMotor:
    def __init__(self, device_info):
        if device_info.get("type").endswith("LargeMotor"):
            self.motor = LargeMotor(ADDRESS_MAP.get(device_info.get("port")))
        else:
            self.motor = MediumMotor(ADDRESS_MAP.get(device_info.get("port")))

    def on_for_rotations(self, speed, rotations, brake=True, block=True):
        """
        Rotate the motor at ``speed`` for ``rotations``
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        """
        return self.motor.on_for_rotations(clamp(speed, -100, 100), rotations, brake, block)

    def on_for_degrees(self, speed, degrees, brake=True, block=True):
        """
        Rotate the motor at ``speed`` for ``degrees``
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        """
        return self.motor.on_for_degrees(clamp(speed, -100, 100), degrees, brake, block)

    def on_to_position(self, speed, position, brake=True, block=True):
        """
        Rotate the motor at ``speed`` to ``position``
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        """
        return self.motor.on_to_position(clamp(speed, -100, 100), position, brake, block)

    def on_for_seconds(self, speed, seconds, brake=True, block=True):
        """
        Rotate the motor at ``speed`` for ``seconds``
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        """
        return self.motor.on_for_seconds(clamp(speed, -100, 100), seconds, brake, block)

    def on(self, speed, brake=True, block=False):
        """
        Rotate the motor at ``speed`` for forever
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        Note that `block` is False by default, this is different from the
        other `on_for_XYZ` methods.
        """
        return self.motor.on(clamp(speed, -100, 100), brake, block)

    def off(self, brake=True):
        return self.motor.off(brake)

    def rotations(self):
        return self.motor.rotations

    def degrees(self):
        return self.motor.degrees
