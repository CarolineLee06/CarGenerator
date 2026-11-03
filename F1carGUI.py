
import importlib
from pyside2 import QtWidgets, QtCore
from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui
import f1car

importlib.reload(f1car)


def get_main_maya_win():
    main_win = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win), QtWidgets.QWidget)


class F1CarGeneratorWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__(parent=get_main_maya_win())
        self.f1_generator = f1car.F1Car()
        self.setWindowTitle("F1 Car Generator")
        self.setWindowFlag(QtCore.Qt.WindowType.Tool)
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
        self.body_length_ui()
        self.body_width_ui()
        self.body_height_ui()
        self.wing_width_ui()
        self.group_name_ui()
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

    @QtCore.Slot()
    def create(self):
        self.f1_generator.length = self.length_dspnbx.value()
        self.f1_generator.width = self.width_dspnbx.value()
        self.f1_generator.height = self.height_dspnbx.value()
        self.f1_generator.wing_width = self.wing_dspnbx.value()
        self.f1_generator.grp_name = self.get_grp_name()
        self.f1_generator.number = self.f1_generator.get_number()
        self.f1_generator.create()

    def get_grp_name(self):
        if self.enablegrpname_cb.isChecked():
            name = self.grpname_le.text().strip()
            if name:
                return name.replace(" ", "_")
        return "F1Car"

    @QtCore.Slot()
    def randomize_color(self):
        self.f1_generator.change_body_color()
