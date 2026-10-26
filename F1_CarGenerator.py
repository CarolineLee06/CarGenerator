import maya.cmds as cmds
import random
from pyside6 import QtWidgets

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


def make_carbody(name, position, size):
    box = cmds.polyCube(
        name=name,
        width=size[0],
        height=size[1],
        depth=size[2],
    )[0]

    cmds.move(position[0], position[1], position[2], box)

    return box


def make_wheel(name, position):
    wheel = cmds.polyCylinder(
        name=name,
        radius=0.5,
        height=0.3,
        axis=(0, 0, 1)
    )[0]

    cmds.move(position[0], position[1], position[2], wheel)

    return wheel

