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
    robot.stop()
    robot.arm_down()
    print("Goodbye")
    ev3.Sound.speak("Goodbye").wait()


main()
