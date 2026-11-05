
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import random

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance


def get_main_maya_win():
    main_win = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win), QtWidgets.QWidget)


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
        self.number = self.get_number()
        self.create_body()
        self.create_cockpit()
        self.create_wings()
        self.create_wheels()
        self.group_car()
        self.create_material()

    def create_body(self):
        name = "carBody_" + str(self.number)
        body = cmds.polyCube(name=name, w=self.width,
                             h=self.height, d=self.length)[0]
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
        front_y = self.wheel_radius + self.height * 0.3
        rear_y = self.wheel_radius + self.height * 1.2
        self.create_wing("frontWing", front_z, front_y)
        self.create_wing("rearWing", rear_z, rear_y)

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
        body = "carBody_" + number
        cmds.sets(body, edit=True, forceElement=shading_group)

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


class F1CarGeneratorGUI(QtWidgets.QDialog):

    def __init__(self):
        super().__init__(parent=get_main_maya_win())
        self.f1_generator = F1Car()
        self.setWindowTitle("F1 Car Generator")
        self.setWindowFlag(QtCore.Qt.Tool)
        self.create_layout()
        self.create_connections()

    def create_layout(self):
        self.main_lay = QtWidgets.QVBoxLayout()
        self._form_ui()
        self.create_btn = QtWidgets.QPushButton("Generate New Car")
        self.color_btn = QtWidgets.QPushButton("Randomize Body Color")
        self.main_lay.addWidget(self.create_btn)
        self.main_lay.addWidget(self.color_btn)
        self.setLayout(self.main_lay)

    def _form_ui(self):
        self.form_lay = QtWidgets.QFormLayout()
        self._body_length_ui()
        self._body_width_ui()
        self._body_height_ui()
        self._wing_width_ui()
        self._group_name_ui()
        self.main_lay.addLayout(self.form_lay)

    def _body_length_ui(self):
        self.length_dspnbx = QtWidgets.QDoubleSpinBox()
        self.length_dspnbx.setRange(2, 8)
        self.length_dspnbx.setValue(self.f1_generator.length)
        self.form_lay.addRow("Body Length", self.length_dspnbx)

    def _body_width_ui(self):
        self.width_dspnbx = QtWidgets.QDoubleSpinBox()
        self.width_dspnbx.setRange(1, 3)
        self.width_dspnbx.setValue(self.f1_generator.width)
        self.form_lay.addRow("Body Width", self.width_dspnbx)

    def _body_height_ui(self):
        self.height_dspnbx = QtWidgets.QDoubleSpinBox()
        self.height_dspnbx.setRange(0.2, 1.5)
        self.height_dspnbx.setValue(self.f1_generator.height)
        self.form_lay.addRow("Body Height", self.height_dspnbx)

    def _wing_width_ui(self):
        self.wing_dspnbx = QtWidgets.QDoubleSpinBox()
        self.wing_dspnbx.setRange(1, 2.5)
        self.wing_dspnbx.setValue(self.f1_generator.wing_width)
        self.form_lay.addRow("Wing Width", self.wing_dspnbx)

    def _group_name_ui(self):
        self.enablegrpname_cb = QtWidgets.QCheckBox()
        self.enablegrpname_cb.setChecked(False)
        self.form_lay.addRow("Enable Group Name", self.enablegrpname_cb)
        self.grpname_le = QtWidgets.QLineEdit()
        self.grpname_le.setText(self.f1_generator.grp_name)
        self.grpname_le.setEnabled(False)
        self.form_lay.addRow("Group Name", self.grpname_le)

    def create_connections(self):
        self.enablegrpname_cb.toggled.connect(self.toggle_grpname_le)
        self.create_btn.clicked.connect(self.create)
        self.color_btn.clicked.connect(self.randomize_color)

    @QtCore.Slot()
    def toggle_grpname_le(self):
        enabled = self.enablegrpname_cb.isChecked()
        self.grpname_le.setEnabled(enabled)

    def get_group_name(self):
        if self.enablegrpname_cb.isChecked():
            name = self.grpname_le.text().strip()
            if name:
                return name.replace(" ", "_")
        return "F1Car"

    @QtCore.Slot()
    def create(self):
        self.f1_generator.length = self.length_dspnbx.value()
        self.f1_generator.width = self.width_dspnbx.value()
        self.f1_generator.height = self.height_dspnbx.value()
        self.f1_generator.wing_width = self.wing_dspnbx.value()
        self.f1_generator.grp_name = self.get_group_name()
        self.f1_generator.create()

    @QtCore.Slot()
    def randomize_color(self):
        self.f1_generator.change_body_color()
