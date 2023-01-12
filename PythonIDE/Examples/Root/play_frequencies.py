#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3

robot = Root(Bluetooth())


@event(robot.when_play)
async def play_frequencies(robot):
    for i in range(1, 20):
        await robot.play_tone(i*100, 0.25)
    await robot.stop_sound()

robot.play()
