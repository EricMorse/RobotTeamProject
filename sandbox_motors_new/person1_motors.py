"""
Functions for moving the robot FORWARD and BACKWARD.
Authors: David Fisher, David Mutchler and Eric Morse.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

# DONE: 2. Implment forward_seconds, then the relevant part of the test function.
#          Test and correct as needed.
#   Then repeat for forward_by_time.
#   Then repeat for forward_by_encoders.
#   Then repeat for the backward functions.

import ev3dev.ev3 as ev3
import time


def test_forward_backward():
    """
    Tests the forward and backward functions, as follows:
      1. Repeatedly:
          -- Prompts for and gets input from the console for:
             -- Seconds to travel
                  -- If this is 0, BREAK out of the loop.
             -- Speed at which to travel (-100 to 100)
             -- Stop action ("brake", "coast" or "hold")
          -- Makes the robot run per the above.
      2. Same as #1, but gets inches and runs forward_by_time.
      3. Same as #2, but runs forward_by_encoders.
      4. Same as #1, 2, 3, but tests the BACKWARD functions.
    """

    # Tests forward_seconds

    # seconds = 1
    # Any value other than 0.
    speed = int(input("Enter a speed for both motors (0 to 100): "))
    seconds = int(input("Enter a time to drive (seconds): "))
    stop_method = input("Enter stop action: ")
    forward_seconds(seconds, speed, stop_method)

    # Tests forward_by_time
    # inches = 1
    inches = int(input("Enter inches for motors"))
    forward_by_time(inches, speed, stop_method)

    # Tests forward by encoders
    # inches = 1
    start = int(input("Start (1 = yes): "))
    if start == 1:
        forward_by_encoders(inches, speed, stop_method)

    # Tests backward_seconds
    start = int(input("Start (1 = yes): "))
    if start == 1:
        backward_seconds(seconds, speed, stop_method)

    # Tests backward_by_time
    start = int(input("Start (1 = yes): "))
    if start == 1:
        backward_by_time(inches, speed, stop_method)

    # Tests backward by encoders
    start = int(input("Start (1 = yes): "))
    if start == 1:
        backward_by_encoders(inches, speed, stop_method)


def forward_seconds(seconds, speed, stop_method):
    """
    Makes the robot move forward for the given number of seconds at the given speed,
    where speed is between -100 (full speed backward) and 100 (full speed forward).
    Uses the given stop_action.
    """

    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    left_motor.stop_action = stop_method
    right_motor.stop_action = stop_method
    left_motor.run_forever(speed_sp=speed*8)
    right_motor.run_forever(speed_sp=speed*8)
    time.sleep(seconds)
    left_motor.stop()
    right_motor.stop()


def forward_by_time(inches, speed, stop_method):
    """
    Makes the robot move forward the given number of inches at the given speed,
    where speed is between -100 (full speed backward) and 100 (full speed forward).
    Uses the algorithm:
      0. Compute the number of seconds to move to achieve the desired distance.
      1. Start moving.
      2. Sleep for the computed number of seconds.
      3. Stop moving.
    """
    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Compute time at given speed and inches
    seconds = (inches * 90) / abs((speed * 8))

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    left_motor.speed_sp = speed * 8
    right_motor.speed_sp = speed * 8
    left_motor.stop_action = stop_method
    right_motor.stop_action = stop_method
    left_motor.time_sp = seconds * 1000
    right_motor.time_sp = seconds * 1000
    left_motor.run_timed()
    right_motor.run_timed()

def forward_by_encoders(inches, speed, stop_method):
    """
    Makes the robot move forward the given number of inches at the given speed,
    where speed is between -100 (full speed backward) and 100 (full speed forward).
    Uses the algorithm:
      1. Compute the number of degrees the wheels should spin to achieve the desired distance.
      2. Move until the computed number of degrees is reached.
    """
    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
    if speed >= 0:
        degrees = inches*90
    else:
        degrees = inches*-90

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    left_motor.speed_sp = speed * 8
    right_motor.speed_sp = speed * 8
    left_motor.stop_action = stop_method
    right_motor.stop_action = stop_method

    left_motor.run_to_rel_pos(position_sp=degrees)
    right_motor.run_to_rel_pos(position_sp=degrees)


def backward_seconds(seconds, speed, stop_method):
    """ Calls forward_seconds with negative speeds to achieve backward motion. """
    forward_seconds(seconds, -1 * speed, stop_method)


def backward_by_time(inches, speed, stop_method):
    """ Calls forward_by_time with negative speeds to achieve backward motion. """
    forward_by_time(inches, -1 * speed, stop_method)


def backward_by_encoders(inches, speed, stop_method):
    """ Calls forward_by_encoders with negative speeds to achieve backward motion. """
    forward_by_encoders(inches, -1 * speed, stop_method)


test_forward_backward()
