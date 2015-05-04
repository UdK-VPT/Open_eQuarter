# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_main_process_dock.ui'
#
# Created: Wed Apr 22 17:01:58 2015
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

class Ui_MainProcess_dock(object):
    def setupUi(self, MainProcess_dock):
        MainProcess_dock.setObjectName(_fromUtf8("MainProcess_dock"))
        MainProcess_dock.resize(374, 516)
        MainProcess_dock.setMinimumSize(QtCore.QSize(374, 500))
        MainProcess_dock.setStyleSheet(_fromUtf8("QListView {"
                                                 "text-align: left;"
                                                 "background-color: #f0f0f0"
                                                 "}"
                                                 "QListView QStandardItemModel QStandardItem {"
                                                 "font-size: 17px;  "
                                                 "}"
"QStandardItem {\n"
"    border: none;\n"
"    margin-left: 2px;\n"
"    min-width: 261px;\n"
"    max-width: 320px;\n"
"    min-height: 32px;\n"
"    max-height: 40px;\n"
"    qproperty-icon: url(\":/Controls/icons/openmark.png\") off,\n"
"                            url(\":/Controls/icons/checkmark.png\") on ;\n"
"    qproperty-iconSize: 17px; \n"
"    qproperty-flat: true;\n"
"    qproperty-checkable: true;\n"
"}\n"
"\n"
"QStandardItem:active {\n"
"    border: none;\n"
"}\n"
"\n"
"#menu_bar {\n"
"    padding: -10px;\n"
"}\n"
"\n"
"\n"
"\n"
""))
        self.dockWidgetContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.menu_bar = QtGui.QWidget(self.dockWidgetContents)
        self.menu_bar.setMinimumSize(QtCore.QSize(60, 0))
        self.menu_bar.setObjectName(_fromUtf8("menu_bar"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.menu_bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.settings_dropdown_btn = QtGui.QToolButton(self.menu_bar)
        self.settings_dropdown_btn.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/gearwheel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_dropdown_btn.setIcon(icon)
        self.settings_dropdown_btn.setIconSize(QtCore.QSize(17, 17))
        self.settings_dropdown_btn.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.settings_dropdown_btn.setObjectName(_fromUtf8("settings_dropdown_btn"))
        self.horizontalLayout.addWidget(self.settings_dropdown_btn)
        self.tools_dropdown_btn = QtGui.QToolButton(self.menu_bar)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/tools.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tools_dropdown_btn.setIcon(icon1)
        self.tools_dropdown_btn.setIconSize(QtCore.QSize(17, 17))
        self.tools_dropdown_btn.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.tools_dropdown_btn.setObjectName(_fromUtf8("tools_dropdown_btn"))
        self.horizontalLayout.addWidget(self.tools_dropdown_btn)
        self.horizontalLayout_3.addWidget(self.menu_bar, QtCore.Qt.AlignLeft)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.active_page_dropdown = QtGui.QComboBox(self.dockWidgetContents)
        self.active_page_dropdown.setObjectName(_fromUtf8("active_page_dropdown"))
        self.horizontalLayout_3.addWidget(self.active_page_dropdown)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.process_page = QtGui.QStackedWidget(self.dockWidgetContents)
        self.process_page.setEnabled(True)
        self.process_page.setMinimumSize(QtCore.QSize(350, 280))
        self.process_page.setMaximumSize(QtCore.QSize(16777215, 280))
        self.process_page.setAutoFillBackground(False)
        self.process_page.setStyleSheet(_fromUtf8(""))
        self.process_page.setFrameShape(QtGui.QFrame.StyledPanel)
        self.process_page.setFrameShadow(QtGui.QFrame.Plain)
        self.process_page.setLineWidth(2)
        self.process_page.setMidLineWidth(1)
        self.process_page.setObjectName(_fromUtf8("process_page"))

        self.verticalLayout_5.addWidget(self.process_page)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.setSpacing(5)
        self.button_layout.setObjectName(_fromUtf8("button_layout"))
        self.pushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.button_layout.addWidget(self.pushButton)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.button_layout.addItem(spacerItem7)
        self.process_button_auto = QtGui.QPushButton(self.dockWidgetContents)
        self.process_button_auto.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/autorun.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.process_button_auto.setIcon(icon2)
        self.process_button_auto.setObjectName(_fromUtf8("process_button_auto"))
        self.button_layout.addWidget(self.process_button_auto)
        self.process_button_prev = QtGui.QPushButton(self.dockWidgetContents)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/arrow_left.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.process_button_prev.setIcon(icon3)
        self.process_button_prev.setObjectName(_fromUtf8("process_button_prev"))
        self.button_layout.addWidget(self.process_button_prev)
        self.process_button_next = QtGui.QPushButton(self.dockWidgetContents)
        self.process_button_next.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/arrow_right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.process_button_next.setIcon(icon4)
        self.process_button_next.setIconSize(QtCore.QSize(16, 16))
        self.process_button_next.setObjectName(_fromUtf8("process_button_next"))
        self.button_layout.addWidget(self.process_button_next)
        self.verticalLayout_5.addLayout(self.button_layout)
        spacerItem8 = QtGui.QSpacerItem(20, 32, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem8)
        self.logo_layout = QtGui.QHBoxLayout()
        self.logo_layout.setObjectName(_fromUtf8("logo_layout"))
        self.oeq_clickable_logo = QClickableLabel(self.dockWidgetContents)
        self.oeq_clickable_logo.setMinimumSize(QtCore.QSize(350, 57))
        self.oeq_clickable_logo.setText(_fromUtf8(""))
        self.oeq_clickable_logo.setPixmap(QtGui.QPixmap(_fromUtf8(":/Brands/icons/OeQ_logo_footer.png")))
        self.oeq_clickable_logo.setObjectName(_fromUtf8("oeq_clickable_logo"))
        self.logo_layout.addWidget(self.oeq_clickable_logo)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.logo_layout.addItem(spacerItem9)
        self.verticalLayout_5.addLayout(self.logo_layout)
        MainProcess_dock.setWidget(self.dockWidgetContents)

        self.retranslateUi(MainProcess_dock)
        self.process_page.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainProcess_dock)

    def retranslateUi(self, MainProcess_dock):
        MainProcess_dock.setWindowTitle(_translate("MainProcess_dock", "Open eQuarter - Analysis", None))
        self.tools_dropdown_btn.setText(_translate("MainProcess_dock", "...", None))
        self.label.setText(_translate("MainProcess_dock", "Currently viewing:", None))
        self.pushButton.setText(_translate("MainProcess_dock", "Cancel", None))
        self.process_button_auto.setToolTip(_translate("MainProcess_dock", "Click this button to autorun the process", None))
        self.process_button_prev.setText(_translate("MainProcess_dock", "Previous", None))
        self.process_button_next.setText(_translate("MainProcess_dock", "Next ", None))

from oeq_ui_classes import QClickableLabel, QProcessButton
import resources_rc
