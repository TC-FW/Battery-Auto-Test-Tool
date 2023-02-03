# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_rule_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import time

from PyQt5 import QtCore, QtGui, QtWidgets


class MyTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        QtWidgets.QTableWidget.__init__(self)

    def dragEvent(self, DragEvent):
        print(self.rowAt(DragEvent.pos().y()))

    def dropEvent(self, DropEvent):
        begin_row = self.currentRow()
        new_row = self.rowAt(DropEvent.pos().y())  # 获取鼠标拖动至TableWidget的行

        if new_row >= 0:
            if begin_row < new_row:
                new_row += 1
            elif begin_row > new_row:
                begin_row += 1
            else:
                return
        else:
            return

        self.insertRow(new_row)
        for i in range(self.columnCount()):
            self.setCellWidget(new_row, i, self.cellWidget(begin_row, i))
        for i in range(self.columnCount()):
            if self.item(begin_row, i) is not None:
                self.setItem(new_row, i, QtWidgets.QTableWidgetItem((self.item(begin_row, i).text())))
        self.removeRow(begin_row)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(1018, 698)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.load_setting_button = QtWidgets.QPushButton(Form)
        self.load_setting_button.setObjectName("load_setting_button")
        self.gridLayout.addWidget(self.load_setting_button, 1, 5, 1, 1)
        self.group_cycle_count_input = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_cycle_count_input.sizePolicy().hasHeightForWidth())
        self.group_cycle_count_input.setSizePolicy(sizePolicy)
        self.group_cycle_count_input.setObjectName("group_cycle_count_input")
        self.gridLayout.addWidget(self.group_cycle_count_input, 6, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 3, 1, 1)
        self.enter_button = QtWidgets.QPushButton(Form)
        self.enter_button.setObjectName("enter_button")
        self.gridLayout.addWidget(self.enter_button, 7, 5, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.file_select_input = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_select_input.sizePolicy().hasHeightForWidth())
        self.file_select_input.setSizePolicy(sizePolicy)
        self.file_select_input.setObjectName("file_select_input")
        self.horizontalLayout_2.addWidget(self.file_select_input)
        self.log_select_button = QtWidgets.QToolButton(Form)
        self.log_select_button.setObjectName("log_select_button")
        self.horizontalLayout_2.addWidget(self.log_select_button)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 5)
        self.dc_init_mode1_v_input = QtWidgets.QLineEdit(Form)
        self.dc_init_mode1_v_input.setObjectName("dc_init_mode1_v_input")
        self.gridLayout.addWidget(self.dc_init_mode1_v_input, 4, 2, 1, 1)
        self.dc_init_mode1_checkbox = QtWidgets.QCheckBox(Form)
        self.dc_init_mode1_checkbox.setObjectName("dc_init_mode1_checkbox")
        self.gridLayout.addWidget(self.dc_init_mode1_checkbox, 4, 0, 1, 1)
        self.log_first_value_combox = QtWidgets.QComboBox(Form)
        self.log_first_value_combox.setEditable(True)
        self.log_first_value_combox.setObjectName("log_first_value_combox")
        self.log_first_value_combox.addItem("")
        self.log_first_value_combox.addItem("")
        self.gridLayout.addWidget(self.log_first_value_combox, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.save_setting_button = QtWidgets.QPushButton(Form)
        self.save_setting_button.setObjectName("save_setting_button")
        self.gridLayout.addWidget(self.save_setting_button, 1, 4, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.add_rule_button = QtWidgets.QPushButton(Form)
        self.add_rule_button.setObjectName("add_rule_button")
        self.horizontalLayout.addWidget(self.add_rule_button)
        self.del_rule_button = QtWidgets.QPushButton(Form)
        self.del_rule_button.setObjectName("del_rule_button")
        self.horizontalLayout.addWidget(self.del_rule_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 6)
        self.rule_table = MyTable(Form)
        self.rule_table.setLineWidth(1)
        self.rule_table.setRowCount(0)
        self.rule_table.setObjectName("rule_table")
        self.rule_table.setColumnCount(11)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.rule_table.setHorizontalHeaderItem(10, item)
        self.rule_table.horizontalHeader().setVisible(True)
        self.rule_table.horizontalHeader().setCascadingSectionResizes(True)
        self.rule_table.horizontalHeader().setDefaultSectionSize(80)
        self.rule_table.horizontalHeader().setHighlightSections(True)
        self.rule_table.horizontalHeader().setMinimumSectionSize(80)
        self.gridLayout.addWidget(self.rule_table, 2, 0, 1, 6)
        self.dc_init_mode1_i_input = QtWidgets.QLineEdit(Form)
        self.dc_init_mode1_i_input.setObjectName("dc_init_mode1_i_input")
        self.gridLayout.addWidget(self.dc_init_mode1_i_input, 4, 4, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 3)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 3)
        self.gridLayout.setColumnStretch(5, 3)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.file_select_input, self.log_select_button)
        Form.setTabOrder(self.log_select_button, self.log_first_value_combox)
        Form.setTabOrder(self.log_first_value_combox, self.save_setting_button)
        Form.setTabOrder(self.save_setting_button, self.load_setting_button)
        Form.setTabOrder(self.load_setting_button, self.rule_table)
        Form.setTabOrder(self.rule_table, self.add_rule_button)
        Form.setTabOrder(self.add_rule_button, self.del_rule_button)
        Form.setTabOrder(self.del_rule_button, self.dc_init_mode1_checkbox)
        Form.setTabOrder(self.dc_init_mode1_checkbox, self.dc_init_mode1_v_input)
        Form.setTabOrder(self.dc_init_mode1_v_input, self.dc_init_mode1_i_input)
        Form.setTabOrder(self.dc_init_mode1_i_input, self.group_cycle_count_input)
        Form.setTabOrder(self.group_cycle_count_input, self.enter_button)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.load_setting_button.setText(_translate("Form", "Load Setting"))
        self.label_3.setText(_translate("Form", "Group循环次数 (空格隔开):"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p align=\"center\">电压(V):</p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p align=\"center\">电流(A): </p></body></html>"))
        self.enter_button.setText(_translate("Form", "OK"))
        self.label_2.setText(_translate("Form", "Log Files:"))
        self.log_select_button.setText(_translate("Form", "..."))
        self.dc_init_mode1_checkbox.setText(_translate("Form", "DC特殊关闭模式"))
        self.log_first_value_combox.setItemText(0, _translate("Form", "Sample"))
        self.log_first_value_combox.setItemText(1, _translate("Form", "Time"))
        self.label.setText(_translate("Form", "<html><head/><body><p>First Value in Log:</p></body></html>"))
        self.save_setting_button.setText(_translate("Form", "Save Setting"))
        self.add_rule_button.setText(_translate("Form", "+"))
        self.del_rule_button.setText(_translate("Form", "-"))
        item = self.rule_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Check"))
        item = self.rule_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Group"))
        item = self.rule_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "C/D/S"))
        item = self.rule_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Stop"))
        item = self.rule_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Judge"))
        item = self.rule_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Value"))
        item = self.rule_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Wait T"))
        item = self.rule_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Limit T"))
        item = self.rule_table.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Mode / V"))
        item = self.rule_table.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Value / C"))
        item = self.rule_table.horizontalHeaderItem(10)
        item.setText(_translate("Form", "EX Command"))
