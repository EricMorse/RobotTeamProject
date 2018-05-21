# Fast and Furious truck delivery program that delivers IR detected object to customer SIG1 (red) blue recycle can
# while avoiding SIG2 (orange) green ball
# IR should be used to grab object, grab when proximity < 10
# Do not use beacon
# avoid drunk width = 21 height = 30
# small blue recycle can deliver height = 130 or width 115 (width may be more reliable)
# it can see the object from far away
#
# This is the ev3 side of the program.
#
# Author: Eric Morse

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    robot = robo.Snatch3r()
    # initialize SIG1 information
    robot.pixy.mode = "SIG1"
    delivered = False
    # set robot arm ot initial position
    robot.arm_down()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    # announce that robot is ready
    while robot.speed == -1:
        robot.detect_objects(mqtt_client)
    print("Ready for package")
    ev3.Sound.speak("Ready for package")
    while (not robot.touch_sensor.is_pressed) and robot.running:
        # If package (blue recycle can) is too far, move closer
        while (robot.ir_sensor.proximity > 8) and robot.running:
            robot.set_forward(0, 0)
        # grab package
        robot.stop()
        robot.arm_up()
    # deliver package to customer while avoiding ball
    while (not delivered) and robot.running:
        robot.avoid_ball(mqtt_client)
        delivered = robot.deliver_package(mqtt_client)
        time.sleep(0.05)

    robot.stop()
    if delivered:
        # announce that delivery was successful
        print("Delivery successful")
        ev3.Sound.speak("Delivery successful")
    else:
        # announce that program was quit
        print("Quit command was called")
        ev3.Sound.speak("Quit command was called")


main()
