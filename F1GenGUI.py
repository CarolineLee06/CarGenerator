import importlib
from pyside2 import QtWidgets, QtCore
from shiboken6 import WrapInstance

import maya.OpenMayaUI as omui

import F1gen
importlib.reload(F1gen)
from F1gen import F1Car


class F1CarGeneratorWindow(QtWidgets.QDialog):
    def __init__(self):
        super(F1CarGeneratorWindow, self).__init__()
        self.setWindowTitle("F1 Car Generator")
        self.setMinimumWidth(350)
        self.setMinimumHeight(300)
        self.create_interface()

    def create_interface(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel("F1 Car Generator")
        title.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title)
        instructions = QtWidgets.QLabel("set body dimensions, generate car")
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        scroll_area = QtWidgets.ScrollArea()
        scroll_area.setWidgetResizeable(True)
        scroll_area.setMinimumHeight(140)
        main_layout.addWidget(scroll_area)

        scroll_content = QtWidgets.QtWidget()
        scroll_area.setWidget(scroll_content)
        settings_layout = QtWidgets.QVBoxLayout(scroll_content)

        settings_layout.addWidget(QtWidgets.QLabel("Body Length"))
        self.body_length_spinbox = QtWidgets.QDoubleSpingBox()
        self.body_length_spinbox.setRange(2.0, 8.0)
        self.body_length_spinbox.setSingleStep(0.1)
        self.body_length_spinbox.setDecimals(2)
        self.body_length_spinbox.setValue(4.0)
        settings_layout.addWidget(self.body_length_spinbox)

        settings_layout.addWidget(QtWidgets.QLabel("Body Width"))
        self.body_width_spinbox = QtWidgets.QDoubleSpingBox()
        self.body_width_spinbox.setRange(1.0, 3.0)
        self.body_width_spinbox.setSingleStep(0.1)
        self.body_width_spinbox.setDecimals(2)
        self.body_width_spinbox.setValue(0.5)
        settings_layout.addWidget(self.body_width_spinbox)

        settings_layout.addWidget(QtWidgets.QLabel("Body Height"))
        self.body_height_spinbox = QtWidgets.QDoubleSpingBox()
        self.body_height_spinbox.setRange(0.2, 1.5)
        self.body_height_spinbox.setSingleStep(0.1)
        self.body_height_spinbox.setDecimals(2)
        self.body_height_spinbox.setValue(0.5)
        settings_layout.addWidget(self.body_height_spinbox)

        settings_layout.addStretch()

        generate_button = QtWidgets.QPushButton("Generate New Car")
        generate_button.clicked.connect(self.generate_car)
        main_layout.addWidget(generate_button)
        color_button = QtWidgets.QPushButton(
            "Randomize Selected Body Color"
        )
        color_button.clicked.connect(self.randomize_selected_color)
        main_layout.addWidget(color_button)

    def generate_car(self):
        body_length = self.body_length_spinbox.value()
        body_width = self.body_width_spinbox.value()
        body_height = self.body_height_spinbox.value()
        car = F1Car(
            body_length=body_length,
            body_width=body_width,
            body_height=body_height
        )
        car.create()

    def randomize_selected_color(self):
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            cmds.warning("select a car body first.")
            return

        body = selection[0].split("|")[-1]
        if not body.startswith("carBody_"):
            cmds.warning("select a car body")
            return

        number = body.replace("carBody_", "")
        if not number.isdigit():
            cmds.warning("could not identify the selcted body")
            return

        material_name = "carMaterial_" + number
        if not cmds.objExists(material_name):
            cmds.warning("The selected body has no material")
            return

        red = random.random()
        green = random.random()
        blue = random.random()

        cmds.setAttr(
            material_name + ".color",
            red,
            green,
            blue,
            type="double3"
        )
        print("car body color changed")


car_generator_window = F1CarGeneratorWindow()
car_generator_window.show()
