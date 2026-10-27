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

    def create_body(self):
        body = cmds.polyCube(
            name="carBody_" + str(self.car_number),
            width=self.body_width,
            height=self.body_height,
            length=self.body_length,
        )[0]
        cmds.move(
            0, self.wheel_radius + self.body_height / 2,
            0,
            body
        )
        self.parts.append(body)

    def create_cockpit(self):
        cockpit = cmds.polyCube(
            name="cockpit_" + str(self.car_number),
            width=self.body_width * 0.45,
            height=self.body_height * 0.8,
            length=self.body_length * 0.3
        )[0]

        cmds.move(
            0, self.wheel_radius + self.body_height * 1.1, 0, cockpit
        )
        self.parts.append(cockpit)

    def create_front_wing(self):
        front_wing = cmds.polyCube(
            name="Frontwing_" + str(self.car_number),
             width=self.body_width * 1.4,
             height=0.12,
             depth=0.25
        )[0]

        cmds.move(
            0, self.wheel_radius + self.body_height * 0.3,
            self.body_length / 2 + 0.25, front_wing
        )
        self.parts.append(front_wing)

    def create_rear_wing(self):
        
