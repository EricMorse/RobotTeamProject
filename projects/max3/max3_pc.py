"""
    This module is the pc part of my final project. The robot will go straight and stop in front of a block. Then I will
    use the tkinter window to choose a routine for it to move. The aim is to reach the termination behind the block.
    After the robot arrives it destination, I will give it a reward and the robot will pick it up.
"""
import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    # mqtt_client = None
    # Create an mqtt_client.
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Make a decision')
    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    # Start button.
    start_bt = ttk.Button(main_frame, text='Start')
    start_bt['command'] = lambda: start_pr(mqtt_client)
    start_bt.grid(row=0, column=0)

    # Quit button.
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=0, column=2)
    q_button["command"] = lambda: quit_program(mqtt_client, True)

    # Direction command, which will choose a way for the robot. There are two directions, left and right.
    direction_entry = ttk.Entry(main_frame, width=15)
    direction_entry.grid(row=2,column=0)

    # Choose button, which receive the command from the entry box.
    choose_bt = ttk.Button(main_frame, text='Choose a direction')
    choose_bt['command'] = lambda: direction(mqtt_client, direction_entry.get())
    choose_bt.grid(row=2, column=2)

    root.mainloop()


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def direction(mqtt_client, direction):
    mqtt_client.send_message("direction", direction)


def start_pr(mqtt_client):
    mqtt_client.send_message("start")


main()