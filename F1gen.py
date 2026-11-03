import maya.cmds as cmds
import random


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
        rear_wing = cmds.polyCube(
            name="Rearwing_" + str(self.car_number),
            width=self.body_width * 1.2,
            height=0.15,
            depth=0.25
        )[0]
        cmds.move(
            0, self.wheel_radius + self.body_height * 1.2,
            -self.body_length / 2 - 0.2,
            rear_wing
        )
        self.parts.append(rear_wing)

    def create_wheels(self):
        wheel_positions = [(-1, 1), (1, 1), (-1, -1), (1, -1)]

        for i, position in enumerate(wheel_positions):
            x_position = position[0] * (
                self.body_width / 2 + self.wheel_radius * 0.4
            )
            z_position = position[1] * self.body_length * 0.3
            wheel = cmds.polyCylinder(
                name="wheel" + str(i + 1) + "_" + str(self.car_number),
                radius=self.wheel_radius,
                height=0.25,
                subdivisionAxis=16
            )[0]
            cmds.rotate(0, 0, 90, wheel)
            cmds.move(x_position, self.wheel_radius, z_position, wheel)
            self.parts.append(wheel)

    def color_body(self):
        body = "carbody_" + str(self.car_number)
        red = random.random()
        green = random.random()
        blue = random.random()
        material = cmds.shadingNode(
            "Lambert", asShader=True, name="carMaterial_" +
            str(self.car_number))
        cmds.setAttr(material + ".color", red, green, blue, type="double3")
        shading_group = cmds.sets(
            renderable=True, nosurfaceshader=True,
            empty=True,
            name="carMaterialSG_" + str(self.car_number))
        cmds.connectAttr(
            material + ".outColor",
            shading_group + ".surfaceShader")
        cmds.sets(body, edit=True, forceElement=shading_group)
