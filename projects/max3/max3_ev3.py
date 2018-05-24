import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    while robot.ir_sensor.proximity >= 20:
        robot.set_forward(200, 200)

    robot.loop_forever()

main()