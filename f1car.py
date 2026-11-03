
import maya.cmds as cmds
import random


class F1Car:

    def __init__(self):
        self.length = 4.0
        self.width = 1.5
        self.height = 0.5
        self.wing_width = 1.4
        self.grp_name = "F1Car"
        self.wheel_radius = 0.5
        self.parts = []
        self.number = self.get_number()

    def get_number(self):
        number = 1
        while cmds.objExists("carBody_" + str(number)):
            number += 1
        return number

    def create(self):
        self.parts = []
        self.create_body()
        self.create_cockpit()
        self.create_wings()
        self.create_wheels()
        self.group_car()
        self.create_material()

    def create_body(self):
        name = "carBody_" + str(self.number)
        body = cmds.polyCube(name=name, w=self.width, h=self.height,
                             d=self.length)[0]
        y = self.wheel_radius + self.height / 2
        cmds.move(0, y, 0, body)
        self.parts.append(body)

    def create_cockpit(self):
        name = "cockpit_" + str(self.number)
        cockpit = cmds.polyCube(name=name, w=self.width * 0.45,
                                h=self.height * 0.8, d=self.length * 0.3)[0]
        y = self.wheel_radius + self.height * 1.1
        cmds.move(0, y, 0, cockpit)
        self.parts.append(cockpit)

    def create_wings(self):
        front_z = self.length / 2 + 0.25
        rear_z = -self.length / 2 - 0.2
        self.create_wing("frontWing", front_z,
                         self.wheel_radius + self.height * 0.3)
        self.create_wing("rearWing", rear_z,
                         self.wheel_radius + self.height * 1.2)

    def create_wing(self, name, z, y):
        name = name + "_" + str(self.number)
        width = self.width * self.wing_width
        wing = cmds.polyCube(name=name, w=width, h=0.12, d=0.25)[0]
        cmds.move(0, y, z, wing)
        self.parts.append(wing)

    def create_wheels(self):
        positions = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
        for i, position in enumerate(positions):
            self.create_wheel(i, position)

    def create_wheel(self, i, position):
        name = "wheel" + str(i + 1) + "_" + str(self.number)
        x = position[0] * (self.width / 2 + self.wheel_radius * 0.4)
        z = position[1] * self.length * 0.3
        wheel = cmds.polyCylinder(name=name, r=self.wheel_radius, h=0.25)[0]
        cmds.rotate(0, 0, 90, wheel)
        cmds.move(x, self.wheel_radius, z, wheel)
        self.parts.append(wheel)

    def group_car(self):
        name = self.grp_name + "_" + str(self.number)
        cmds.group(self.parts, name=name)

    def create_material(self):
        number = str(self.number)
        material = cmds.shadingNode("lambert", asShader=True,
                                    name="carMaterial_" + number)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True,
                                  empty=True, name="carSG_" + number)
        cmds.connectAttr(material + ".outColor",
                         shading_group + ".surfaceShader", force=True)
        self.random_color(material)
        cmds.sets("carBody_" + number, edit=True, forceElement=shading_group)

    def random_color(self, material):
        color = [random.random(), random.random(), random.random()]
        cmds.setAttr(material + ".color", *color, type="double3")

    def change_body_color(self):
        selection = cmds.ls(selection=True, long=False)
        if not selection:
            cmds.warning("Select a car body first.")
            return
        body = selection[0].split("|")[-1]
        if not body.startswith("carBody_"):
            cmds.warning("Please select a car body.")
            return
        number = body.replace("carBody_", "")
        material = "carMaterial_" + number
        if cmds.objExists(material):
            self.random_color(material)
