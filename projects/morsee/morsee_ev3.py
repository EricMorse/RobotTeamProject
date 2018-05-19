import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com
# Fast and Furious truck delivery program that delivers IR detected object to customer SIG1 (red) blue recycle can
# while avoiding SIG2 (orange) green ball
# IR should be used to grab object, grab when proximity < 10 (grab works)
# Do not use beacon
# customer drop x =  163 y = 110 width = 21 height = 30
# avoid drunk width = 21 height = 30

# if not detect on pixy height = 0
# small blue recycle can deliver height = 130 or width 115 (width may be more reliable)
# it can see the object from far away


class MyDelegate(object):

    def __init__(self, dance_tag):
        self.dance = dance_tag


def main():
    robot = robo.Snatch3r()
    # initialize SIG1 information
    robot.pixy.mode = "SIG1"
    delivered = False
    # drink_width = robot.pixy.value(3)
    # drink_height = robot.pixy.value(4)
    robot.arm_down()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    print("Ready for package")
    ev3.Sound.speak("Ready for package")
    while not robot.touch_sensor.is_pressed:
        # search for package
        # move to drink
        while robot.ir_sensor.proximity > 10:
            robot.set_forward(400, 400)
        # grab drink
        robot.stop()
        robot.arm_up()
        # deliver package to customer while avoiding ball
    while not delivered:
        # my_delegate = MyDelegate(dance_tag)
        robot.avoid_ball(mqtt_client)
        delivered = robot.deliver_package(mqtt_client)
        if not robot.running:
            break
        time.sleep(0.5)

    robot.stop()
    print("Goodbye")
    ev3.Sound.speak("Goodbye")


main()
