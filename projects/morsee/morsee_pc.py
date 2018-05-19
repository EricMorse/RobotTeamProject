import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):

    def __init__(self, canvas, rectangle_tag, oval_tag):
        self.canvas = canvas
        self.rectangle_tag = rectangle_tag
        self.oval_tag = oval_tag

    def on_rectangle_update(self, x, y, width, height):
        self.canvas.coords(self.rectangle_tag, [2*x, 2*y, 2*(x + width), 2*(y + height)])

    def on_oval_update(self, x, y, width, height):
        self.canvas.coords(self.oval_tag, [2*x, 2*y, 2*(x + width), 2*(y + height)])


def main():
    root = tkinter.Tk()
    root.title = "Pixy display"

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    # The values from the Pixy range from 0 to 319 for the x and 0 to 199 for the y.
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=640, height=400)
    canvas.grid(columnspan=2)

    rect_tag = canvas.create_rectangle(0, 0, 0, 0, fill="blue")
    oval_tag = canvas.create_oval(0, 0, 0, 0, fill="green")
    # Buttons for quit and dance
    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=0)
    quit_button["command"] = lambda: quit_program(mqtt_client, True)

    dance_button = ttk.Button(main_frame, text="Dance")
    dance_button.grid(row=3, column=1)
    dance_button["command"] = lambda: dance(mqtt_client)

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


def dance(mqtt_client):
    print("dance")
    mqtt_client.send_message("dance")


main()
