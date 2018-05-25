"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.MAX_SPEED = 900
        self.speed = -1
        self.running = True
        self.ir_sensor = ev3.InfraredSensor()
        self.color_sensor = ev3.ColorSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

        assert self.pixy
        assert self.color_sensor
        assert self.ir_sensor
        assert self.arm_motor.connected
        assert self.touch_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected

    # causes robot to move forward set number of inches
    def forward(self, inches, speed=100, stop_action='brake'):
        k = 360 / 4.5
        degrees = k * inches
        # uses speed argument value for speed
        if self.speed == -1:
            self.left_motor.run_to_rel_pos(speed_sp=8*speed,
                                           position_sp=degrees,
                                           stop_action=stop_action)
            self.right_motor.run_to_rel_pos(speed_sp=8*speed,
                                            position_sp=degrees,
                                            stop_action=stop_action)
        # uses speed button value for speed instead
        else:
            self.left_motor.run_to_rel_pos(speed_sp=self.speed,
                                           position_sp=degrees,
                                           stop_action=stop_action)
            self.right_motor.run_to_rel_pos(speed_sp=self.speed,
                                            position_sp=degrees,
                                            stop_action=stop_action)

        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")

    # causes robot to move forward set number of inches
    def backward(self, inches, speed=100, stop_action='brake'):
        k = 360 / 4.5
        degrees = -1 * k * inches
        self.left_motor.run_to_rel_pos(speed_sp=8*speed,
                                       position_sp=degrees,
                                       stop_action=stop_action)
        self.right_motor.run_to_rel_pos(speed_sp=8*speed,
                                        position_sp=degrees,
                                        stop_action=stop_action)

        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")

    def spin_left(self, inches, speed=100, stop_action='brake'):
        k = 360 / 4.5
        degrees = k * inches
        # uses speed argument value for speed
        if self.speed == -1:
            self.left_motor.run_to_rel_pos(speed_sp=8*speed,
                                           position_sp=-1*degrees,
                                           stop_action=stop_action)
            self.right_motor.run_to_rel_pos(speed_sp=8*speed,
                                            position_sp=degrees,
                                            stop_action=stop_action)
        else:
            # uses speed button value for speed instead
            self.left_motor.run_to_rel_pos(speed_sp=self.speed,
                                           position_sp=-1 * degrees,
                                           stop_action=stop_action)
            self.right_motor.run_to_rel_pos(speed_sp=self.speed,
                                            position_sp=degrees,
                                            stop_action=stop_action)

        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")

    def spin_right(self, inches, speed=100, stop_action='brake'):
        k = 360 / 4.5
        degrees = k * inches
        # uses speed argument value for speed
        if self.speed == -1:
            self.left_motor.run_to_rel_pos(speed_sp=8*speed,
                                           position_sp=degrees,
                                           stop_action=stop_action)
            self.right_motor.run_to_rel_pos(speed_sp=8*speed,
                                            position_sp=-1*degrees,
                                            stop_action=stop_action)
        else:
            # uses speed button value for speed instead
            self.left_motor.run_to_rel_pos(speed_sp=self.speed,
                                           position_sp=degrees,
                                           stop_action=stop_action)
            self.right_motor.run_to_rel_pos(speed_sp=self.speed,
                                            position_sp=-1 * degrees,
                                            stop_action=stop_action)

        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")

    def turn_left(self, inches, speed=100, stop_action='brake'):
        k = 360 / 4.5
        degrees = k * inches
        self.left_motor.run_to_rel_pos(speed_sp=1,
                                       position_sp=1,
                                       stop_action=stop_action)
        self.right_motor.run_to_rel_pos(speed_sp=8 * speed,
                                        position_sp=degrees,
                                        stop_action=stop_action)

        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")

    def turn_right(self, inches, speed=100, stop_action='brake'):
        k = 360 / 4.5
        degrees = k * inches
        self.left_motor.run_to_rel_pos(speed_sp=8*speed,
                                       position_sp=degrees,
                                       stop_action=stop_action)
        self.right_motor.run_to_rel_pos(speed_sp=1,
                                        position_sp=1,
                                        stop_action=stop_action)

        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")

    # calibrates the robot arm
    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()
        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range * 360)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    # raises the robot arm
    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    # lowers the robot arm
    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=-14.2, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.
            if self.touch_sensor.is_pressed:    # The program ends.
                time.sleep(0.5)
                self.arm_up()
                time.sleep(1)
                ev3.Sound.speak("Thank you!").wait()
                self.shutdown()

    def shutdown(self):
        # Modify a variable that will allow the loop_forever method to end. Additionally stop motors and set LEDs green.
        # The most important part of this method is given here, but you should add a bit more to stop motors, etc.
        self.arm_motor.stop(stop_action="brake")
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")
        ev3.Sound.speak("Goodbye").wait()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        self.running = False

    # sets the robot to move forward
    def set_forward(self, left_speed, right_speed):
        # uses speed argument value for speed
        if self.speed == -1:
            self.left_motor.run_forever(speed_sp=left_speed)
            self.right_motor.run_forever(speed_sp=right_speed)
        else:
            # uses speed button value for speed instead
            self.left_motor.run_forever(speed_sp=self.speed)
            self.right_motor.run_forever(speed_sp=self.speed)

    # sets the robot to move backwards
    def set_back(self, left_speed, right_speed, stop_action="brake"):
        # uses speed argument value for speed
        if self.speed == -1:
            self.left_motor.run_forever(speed_sp=-1*int(left_speed), stop_action=stop_action)
            self.right_motor.run_forever(speed_sp=-1*int(right_speed), stop_action=stop_action)
        else:
            # uses speed button value for speed instead
            self.left_motor.run_forever(speed_sp=-1*self.speed, stop_action=stop_action)
            self.right_motor.run_forever(speed_sp=-1*self.speed, stop_action=stop_action)

    # sets the robot to spin to the left
    def set_left(self, left_speed, right_speed, stop_action="brake"):
        # uses speed argument value for speed
        if self.speed == -1:
            left = -1*int(left_speed)
            right = right_speed
        else:
            # uses speed button value for speed instead
            left = -1*int(self.speed)
            right = self.speed
        # runs the motors
        self.left_motor.run_forever(speed_sp=left, stop_action=stop_action)
        self.right_motor.run_forever(speed_sp=right, stop_action=stop_action)

    # sets the robot to spin to the right
    def set_right(self, left_speed, right_speed, stop_action="brake"):
        # uses speed argument value for speed
        if self.speed == -1:
            left = left_speed
            right = -1*int(right_speed)
        else:
            # uses speed button value for speed instead
            right = -1*int(self.speed)
            left = self.speed
        self.left_motor.run_forever(speed_sp=left, stop_action=stop_action)
        self.right_motor.run_forever(speed_sp=right, stop_action=stop_action)

    # stops the motors
    def set_stop(self):
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

    # stops the motors
    def stop(self):
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

    # seeks out the beacon
    def seek_beacon(self):
        beacon_seeker = ev3.BeaconSeeker()
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = beacon_seeker.heading
            current_distance = beacon_seeker.distance
            if current_distance == -128:
                print('IR Remote not found. Distance is -128')
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    print('On the right heading. Distance: ', current_distance)

                    if current_distance <= 20:
                        return True
                    else:
                        self.set_forward(forward_speed, forward_speed)

                elif math.fabs(current_heading) < 10:
                    print('Adjusting heading: ', current_heading)
                    if current_heading < 0:
                        self.set_left(turn_speed, turn_speed)
                    else:
                        self.set_right(turn_speed, turn_speed)

                else:
                    print('Heading is too far off to fix: ', current_heading)
            time.sleep(0.2)
            self.stop()

        print('Abandon ship!')
        self.stop()
        return False

    # steers robot away from the colored ball that is seen on pixy camera
    def avoid_ball(self, mqtt_client):
        # initializes detected_state to false, since it hasn't tried to detect yet
        detected_state = False
        try:
            # switches pixy mode to SIG2 to detect color
            self.pixy.mode = "SIG2"
            # sends detected ball information to pc
            mqtt_client.send_message("on_oval_update",
                                     [self.pixy.value(1), self.pixy.value(2), self.pixy.value(3),
                                      self.pixy.value(4)])
            print("SIG2 x={},y={},width= {},height={}".format(self.pixy.value(1), self.pixy.value(2),
                                                              self.pixy.value(3), self.pixy.value(4)))
            if self.pixy.value(4) >= 1 and self.running:
                detected_state = True
                ev3.Sound.speak("Danger Will Robinson").wait()
                mqtt_client.send_message("on_oval_update",
                                         [self.pixy.value(1), self.pixy.value(2), self.pixy.value(3),
                                          self.pixy.value(4)])
            elif self.running:
                # ball was not detected, send 0 values to remove ball from pc window
                mqtt_client.send_message("on_oval_update", [0, 0, 0, 0])
            while detected_state and self.running:
                # ball was detected, send values to display ball on pc window
                mqtt_client.send_message("on_oval_update",
                                         [self.pixy.value(1), self.pixy.value(2), self.pixy.value(3),
                                          self.pixy.value(4)])
                if self.pixy.value(1) < 130 and self.pixy.value(4) >= 1:
                    # ball is left of robot, spin right to look away from ball
                    self.stop()
                    self.set_right(400, 400)
                    time.sleep(1)
                    self.forward(2)
                elif self.pixy.value(1) > 190 and self.pixy.value(4) >= 1:
                    # ball is right of the robot, spin left to look away from the ball
                    self.stop()
                    self.set_left(400, 400)
                    time.sleep(1)
                    self.forward(2)
                elif self.pixy.value(4) == 0:
                    # robot no longer sees ball, move forward 8 inches so that robot can move around ball
                    self.stop()
                    self.forward(8)
                    ev3.Sound.speak("Danger averted").wait()
                    detected_state = False
                    self.stop()
                time.sleep(0.2)
        except ValueError:
            print("Nothing detected")
            mqtt_client.send_message("on_oval_update", [0, 0, 0, 0])
        time.sleep(0.2)

    # seeks SIG1 object to deliver package to
    def deliver_package(self, mqtt_client):
        if self.running:
            self.pixy.mode = "SIG1"
            mqtt_client.send_message("on_rectangle_update", [self.pixy.value(1), self.pixy.value(2), self.pixy.value(3),
                                                             self.pixy.value(4)])
            if 130 <= self.pixy.value(1) <= 190 and (self.pixy.value(4) >= 115 or self.pixy.value(3) >= 100):
                # robot is directly in front of the SIG1 object, lower arms to deliver package
                self.stop()
                self.arm_down()
                return True
            else:
                if 0 < self.pixy.value(3) < 100:
                    # robot is pointed at SIG1, move forward to it
                    self.stop()
                    self.set_forward(400, 400)
                elif self.pixy.value(1) < 130:
                    # robot is pointed left of SIG1, spin left to point at it
                    self.stop()
                    self.set_left(400, 400)
                else:
                    # robot is pointed right of SIG1, spin right to point at it
                    self.stop()
                    self.set_right(400, 400)

            time.sleep(0.2)

    # shutdown the robot by stopping it, and setting its arm down, before completing shutdown
    def shutdown_new(self):
        self.stop()
        self.arm_down()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        self.running = False

    # takes user input from pc to change the robot speed
    def set_speed(self, speed_value):
        print("speed = {}".format(speed_value))
        self.speed = int(speed_value)

    def detect_objects(self, mqtt_client):
        self.pixy.mode = "SIG1"
        mqtt_client.send_message("on_rectangle_update", [self.pixy.value(1), self.pixy.value(2), self.pixy.value(3),
                                                         self.pixy.value(4)])
        time.sleep(0.1)
        self.pixy.mode = "SIG2"
        mqtt_client.send_message("on_oval_update",
                                 [self.pixy.value(1), self.pixy.value(2), self.pixy.value(3),
                                  self.pixy.value(4)])
        time.sleep(0.1)

    # Robot response to the direction command
    def direction(self, dirctn):
        if dirctn == 1:
            while self.color_sensor.reflected_light_intensity > 70:
                self.set_left(200, 200)
            while self.color_sensor.color != 5:
                if self.color_sensor.reflected_light_intensity > 85:
                    self.turn_left(1.5)
                    self.forward(0.1)
                elif self.color_sensor.reflected_light_intensity < 10:
                    self.turn_right(1.5)
                    self.forward(0.1)
                else:
                    self.set_forward(200, 200)

                time.sleep(0.01)

        elif dirctn == 2:
            while self.color_sensor.reflected_light_intensity > 80:
                self.set_right(200, 200)
            while self.color_sensor.color != 5:
                if self.color_sensor.reflected_light_intensity > 85:
                    self.turn_right(1.5)
                elif self.color_sensor.reflected_light_intensity < 10:
                    self.turn_left(1.5)
                else:
                    self.set_forward(200, 200)
                    time.sleep(0.01)

        # Move to the destination following the line. Destination: the green card, which hue is about 20.
        self.set_stop()

    # Avoid the block
    def start(self):
        while self.ir_sensor.proximity > 3 or self.ir_sensor.proximity == -128:
            self.set_forward(200, 200)
            time.sleep(0.01)
        self.set_stop()

