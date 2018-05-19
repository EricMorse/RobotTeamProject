import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com
# Fast and Furious truck delivery program that delivers IR detected object to Beacon (customer), but avoids
# SIG1(red) green ball and SIG2 (orange) orange ball (Fast and Furious gang)
# if  ball height is 30 or greater, if orange.x < 150 spin right and move forward, else spin left and move

# user sees all objects on window and warns truck of incoming ball
# IR should be used to grab object, grab when proximity < 10
# customer should be beacon
# customer drop x =  163 y = 110 width = 21 height = 30
# avoid drunk width = 21 height = 30
def main():
    robot = robo.Snatch3r()
    # initialize SIG1 information
    robot.pixy.mode = "SIG1"
    # drink_width = robot.pixy.value(3)
    # drink_height = robot.pixy.value(4)
    far_from_customer = True
    while not robot.touch_sensor.is_pressed:
        # search for package

        # move to drink
        while robot.ir_sensor > 10:
            robot.set_forward(400, 400)
        # grab drink
        robot.stop()
        robot.arm_up()
        # search for customer
        while far_from_customer:
            far_from_customer = not robot.seek_beacon()
        robot.arm_down()
        # check if drunk on path, if so, avoid and re-search for customer, if not, move towards customer

        # print("(X, Y)=({}, {}) Width={} Height={} distance={}".format(robot.pixy.value(1), robot.pixy.value(2), robot.pixy.value(3),
        #                                                   robot.pixy.value(4), robot.ir_sensor.proximity))
        time.sleep(0.5)

    print("Goodbye")
    ev3.Sound.speak("Goodbye").wait()


main()
