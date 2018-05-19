import ev3dev.ev3 as ev3
import time
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    # initialize SIG1 information
    robot.pixy.mode = "SIG1"
    #delivered = False
    #while not delivered:
    #    delivered = robot.deliver_package()
    #
    while not robot.touch_sensor.is_pressed:
        robot.avoid_ball()
    print("Goodbye")
    ev3.Sound.speak("Goodbye").wait()


main()
