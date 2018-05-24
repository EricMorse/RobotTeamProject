import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

#    if robot.touch_sensor.is_pressed:
 #       pickup_reward(mqtt_client)

    robot.loop_forever()


def pickup_reward(robot):
    robot.arm_up()
    ev3.Sound.speak("Thank you!").wait()
    robot.shutdown()


main()
