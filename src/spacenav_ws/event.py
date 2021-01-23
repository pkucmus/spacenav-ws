from dataclasses import dataclass
from typing import List, Union


@dataclass
class MotionEvent:
    x: int
    y: int
    z: int
    pitch: int
    yaw: int
    roll: int
    period: int
    type: str = "mtn"

    def to_3dconn(self):
        # here we can do some calculations and return the payloads 
        # Onshape my want
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "pitch": self.pitch,
            "yaw": self.yaw,
            "roll": self.roll,
            "period": self.period,
            "type": self.type,
        }


@dataclass
class ButtonEvent:
    button_id: int
    pressed: bool
    type: str = "btn"

    def to_3dconn(self):
        return {
            "button_id": self.button_id,
            "pressed": self.pressed,
            "type": self.type,
        }


def from_message(message: List[int]) -> Union[MotionEvent, ButtonEvent]:
    if message[0] == 0:
        return MotionEvent(
            x=message[1],
            z=message[2],
            y=message[3],
            pitch=message[4],
            yaw=message[5],
            roll=message[6],
            period=message[7],
        )
    return ButtonEvent(
        button_id=message[1],
        pressed=True if message[0] == 1 else False,
    )

