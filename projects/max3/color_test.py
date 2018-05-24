import ev3dev.ev3 as ev3
import time

import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    while True:
        print(robot.color_sensor.reflected_light_intensity)
        time.sleep(1)


main()
