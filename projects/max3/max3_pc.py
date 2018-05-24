"""
    This module is my final project. It
"""
import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com

mqtt_client = com.MqttClient()
mqtt_client.connect_to_ev3()

root = tkinter.Tk()
root.title('Make a decision')
main_frame = ttk.Frame(root, padding=20)
main_frame.grid()

q_button = ttk.Button(main_frame, text="Quit")
q_button.grid(row=3, column=1)
q_button["command"] = lambda: quit_program(mqtt_client, True)

direction_entry = ttk.Entry(main_frame, width=10)
direction_entry.grid(row=0,column=1)

choose_bt = ttk.Button(main_frame, text='Choose a direction')
choose_bt['command'] = lambda: direction(mqtt_client, direction_entry.get())
choose_bt.grid(row=0, column=2)

root.mainloop()


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def direction(mqtt_client, direction):
    mqtt_client.send_message("dirction", direction)