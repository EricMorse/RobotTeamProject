import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):

    def __init__(self, canvas, rectangle_tag, oval_tag):
        self.canvas = canvas
        self.rectangle_tag = rectangle_tag
        self.oval_tag = oval_tag

    def on_rectangle_update(self, x, y, width, height):
        self.canvas.coords(self.rectangle_tag, [3*x, 3*y, 3*(x + width), 3*(y + height)])

    def on_oval_update(self, x, y, width, height):
        self.canvas.coords(self.oval_tag, [3*x, 3*y, 3*(x + width), 3*(y + height)])


def main():
    root = tkinter.Tk()
    root.title = "Pixy display"

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    # The values from the Pixy range from 0 to 319 for the x and 0 to 199 for the y.
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=960, height=600)
    canvas.grid(columnspan=4)

    rect_tag = canvas.create_rectangle(0, 0, 0, 0, fill="blue")
    oval_tag = canvas.create_oval(0, 0, 0, 0, fill="green")
    # Buttons for quit and dance
    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=3)
    quit_button["command"] = lambda: quit_program(mqtt_client, True)

    set_speed_label = ttk.Label(main_frame, text="Enter speed (0 to 900)")
    set_speed_label.grid(row=3, column=0)
    set_speed_label_entry = ttk.Entry(main_frame, width=8)
    set_speed_label_entry.insert(0, "400")
    set_speed_label_entry.grid(row=3, column=1)

    set_speed_button = ttk.Button(main_frame, text="Set speed")
    set_speed_button.grid(row=3, column=2)
    set_speed_button["command"] = lambda: set_speed(mqtt_client, set_speed_label_entry)

    # Create an MQTT connection
    my_delegate = MyDelegate(canvas, rect_tag, oval_tag)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()
    # mqtt_client.connect_to_ev3("35.194.247.175")  # Off campus IP address of a GCP broker

    root.mainloop()


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown_new")
        mqtt_client.send_message("shutdown_new")
    mqtt_client.close()
    exit()


def set_speed(mqtt_client, set_speed_label_entry):
    print("sent speed = {}".format(set_speed_label_entry.get()))
    mqtt_client.send_message("set_speed", [set_speed_label_entry.get()])


main()
