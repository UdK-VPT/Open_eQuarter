# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_estimated_energy_demand_dialog.ui'
#
# Created: Mon Aug  3 17:56:39 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_EstimatedEnergyDemand_dialog(object):
    def setupUi(self, EstimatedEnergyDemand_dialog):
        EstimatedEnergyDemand_dialog.setObjectName(_fromUtf8("EstimatedEnergyDemand_dialog"))
        EstimatedEnergyDemand_dialog.resize(408, 423)
        self.verticalLayout = QtGui.QVBoxLayout(EstimatedEnergyDemand_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(EstimatedEnergyDemand_dialog)
        self.label.setMaximumSize(QtCore.QSize(376, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_7 = QtGui.QLabel(EstimatedEnergyDemand_dialog)
        self.label_7.setMinimumSize(QtCore.QSize(130, 0))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)
        self.input_layer = QtGui.QComboBox(EstimatedEnergyDemand_dialog)
        self.input_layer.setMinimumSize(QtCore.QSize(240, 0))
        self.input_layer.setObjectName(_fromUtf8("input_layer"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.input_layer)
        self.verticalLayout.addLayout(self.formLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(EstimatedEnergyDemand_dialog)
        self.label_2.setMinimumSize(QtCore.QSize(120, 0))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.area = QtGui.QComboBox(EstimatedEnergyDemand_dialog)
        self.area.setMinimumSize(QtCore.QSize(240, 0))
        self.area.setObjectName(_fromUtf8("area"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.area)
        self.label_3 = QtGui.QLabel(EstimatedEnergyDemand_dialog)
        self.label_3.setMinimumSize(QtCore.QSize(120, 0))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.perimeter = QtGui.QComboBox(EstimatedEnergyDemand_dialog)
        self.perimeter.setMinimumSize(QtCore.QSize(240, 0))
        self.perimeter.setObjectName(_fromUtf8("perimeter"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.perimeter)
        self.label_4 = QtGui.QLabel(EstimatedEnergyDemand_dialog)
        self.label_4.setMinimumSize(QtCore.QSize(120, 0))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.height = QtGui.QComboBox(EstimatedEnergyDemand_dialog)
        self.height.setEnabled(False)
        self.height.setMinimumSize(QtCore.QSize(240, 0))
        self.height.setObjectName(_fromUtf8("height"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.height)
        self.label_5 = QtGui.QLabel(EstimatedEnergyDemand_dialog)
        self.label_5.setMinimumSize(QtCore.QSize(130, 0))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.yoc = QtGui.QComboBox(EstimatedEnergyDemand_dialog)
        self.yoc.setEnabled(True)
        self.yoc.setMinimumSize(QtCore.QSize(240, 0))
        self.yoc.setObjectName(_fromUtf8("yoc"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.yoc)
        self.label_6 = QtGui.QLabel(EstimatedEnergyDemand_dialog)
        self.label_6.setMinimumSize(QtCore.QSize(120, 0))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.floors = QtGui.QComboBox(EstimatedEnergyDemand_dialog)
        self.floors.setMinimumSize(QtCore.QSize(240, 0))
        self.floors.setObjectName(_fromUtf8("floors"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.floors)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_8 = QtGui.QLabel(EstimatedEnergyDemand_dialog)
        self.label_8.setMinimumSize(QtCore.QSize(130, 0))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_8)
        self.output_layer = QtGui.QComboBox(EstimatedEnergyDemand_dialog)
        self.output_layer.setMinimumSize(QtCore.QSize(240, 0))
        self.output_layer.setObjectName(_fromUtf8("output_layer"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.output_layer)
        self.label_9 = QtGui.QLabel(EstimatedEnergyDemand_dialog)
        self.label_9.setMinimumSize(QtCore.QSize(130, 0))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_9)
        self.field_name = QtGui.QLineEdit(EstimatedEnergyDemand_dialog)
        self.field_name.setMinimumSize(QtCore.QSize(230, 0))
        self.field_name.setObjectName(_fromUtf8("field_name"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.field_name)
        self.verticalLayout.addLayout(self.formLayout_3)
        self.dialogButtonBox = QtGui.QDialogButtonBox(EstimatedEnergyDemand_dialog)
        self.dialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dialogButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.dialogButtonBox.setCenterButtons(True)
        self.dialogButtonBox.setObjectName(_fromUtf8("dialogButtonBox"))
        self.verticalLayout.addWidget(self.dialogButtonBox)

        self.retranslateUi(EstimatedEnergyDemand_dialog)
        QtCore.QObject.connect(self.dialogButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EstimatedEnergyDemand_dialog.accept)
        QtCore.QObject.connect(self.dialogButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EstimatedEnergyDemand_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EstimatedEnergyDemand_dialog)

    def retranslateUi(self, EstimatedEnergyDemand_dialog):
        EstimatedEnergyDemand_dialog.setWindowTitle(_translate("EstimatedEnergyDemand_dialog", "Dialog", None))
        self.label.setText(_translate("EstimatedEnergyDemand_dialog", "Calculate the energy demand", None))
        self.label_7.setText(_translate("EstimatedEnergyDemand_dialog", "Input Layer: ", None))
        self.label_2.setText(_translate("EstimatedEnergyDemand_dialog", "Area", None))
        self.label_3.setText(_translate("EstimatedEnergyDemand_dialog", "Perimeter", None))
        self.label_4.setText(_translate("EstimatedEnergyDemand_dialog", "Building Height", None))
        self.label_5.setText(_translate("EstimatedEnergyDemand_dialog", "Year of construction", None))
        self.label_6.setText(_translate("EstimatedEnergyDemand_dialog", "Floors", None))
        self.label_8.setText(_translate("EstimatedEnergyDemand_dialog", "Output Layer:", None))
        self.label_9.setText(_translate("EstimatedEnergyDemand_dialog", "Output fieldname:", None))

