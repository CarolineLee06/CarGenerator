import maya.cmds as cmds
import random
from PySide2 import QtWidgets, QtCore

# create a GUI window that asks for imput from the user, generate car and
# assign random color, make it a button.
# create the body of the f1 car, make a cube
# create the wheels of the f1 car, make cylinders
# generate the wings and the details of the car
# Give the car a random color shader
# Create a shader group to organize shaders, if not already created
# Apply the material to the car
# create the car
# make sure the cars can be generated and dont delete the car group before them
# Give the cars names, F1_Car_01, 02, 03, etc.
# Run generator

class F1Car:
    def __init__(self, body_length=4.0, body_width=1.5,
                 body_height=0.5, wheel_radius=0.5):
        self.body_length = body_length
        self.body_width = body_width
        self.body_height = body_height
        self.wheel_radius = wheel_radius
        self.parts = []

    def create(self):
        number = 1 
        while cmds.objExists("F1Car_" + str(number)):
            number += 1
        self.car_number = number
        self.parts = []

        self.create_body()
        self.create_cockpit()
        self.create_front_wing()
        self.create_rear_wing()
        self.create_wheels()

        self.car_group = cmds.group(
            self.parts, 
            name="F1Car_" + str(self.car_number)
        )
        self.color_body()
        cmds.select(self.car_group)
        print("Created F1Car_" + str(self.car_number))
