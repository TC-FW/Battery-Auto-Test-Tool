# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1019, 699)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.test_stop_button = QtWidgets.QPushButton(Form)
        self.test_stop_button.setObjectName("test_stop_button")
        self.gridLayout_2.addWidget(self.test_stop_button, 2, 1, 1, 1)
        self.test_start_button = QtWidgets.QPushButton(Form)
        self.test_start_button.setObjectName("test_start_button")
        self.gridLayout_2.addWidget(self.test_start_button, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.monitor_table = QtWidgets.QTableWidget(Form)
        self.monitor_table.setObjectName("monitor_table")
        self.monitor_table.setColumnCount(0)
        self.monitor_table.setRowCount(0)
        self.verticalLayout_2.addWidget(self.monitor_table)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.test_status_table = QtWidgets.QTableWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.test_status_table.sizePolicy().hasHeightForWidth())
        self.test_status_table.setSizePolicy(sizePolicy)
        self.test_status_table.setObjectName("test_status_table")
        self.test_status_table.setColumnCount(1)
        self.test_status_table.setRowCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.test_status_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.test_status_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.test_status_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.test_status_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.test_status_table.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.test_status_table.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.test_status_table.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.test_status_table.setHorizontalHeaderItem(0, item)
        self.test_status_table.horizontalHeader().setDefaultSectionSize(300)
        self.test_status_table.horizontalHeader().setMinimumSectionSize(30)
        self.verticalLayout_2.addWidget(self.test_status_table)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(2, 10)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 9)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.register_table = QtWidgets.QTableWidget(Form)
        self.register_table.setRowCount(0)
        self.register_table.setObjectName("register_table")
        self.register_table.setColumnCount(0)
        self.register_table.horizontalHeader().setCascadingSectionResizes(True)
        self.register_table.horizontalHeader().setDefaultSectionSize(150)
        self.register_table.horizontalHeader().setMinimumSectionSize(100)
        self.verticalLayout.addWidget(self.register_table)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.device_data_refresh_button = QtWidgets.QPushButton(Form)
        self.device_data_refresh_button.setObjectName("device_data_refresh_button")
        self.horizontalLayout.addWidget(self.device_data_refresh_button)
        self.device_data_scan_checkbox = QtWidgets.QCheckBox(Form)
        self.device_data_scan_checkbox.setObjectName("device_data_scan_checkbox")
        self.horizontalLayout.addWidget(self.device_data_scan_checkbox)
        self.scan_time_combobox = QtWidgets.QComboBox(Form)
        self.scan_time_combobox.setEditable(False)
        self.scan_time_combobox.setObjectName("scan_time_combobox")
        self.scan_time_combobox.addItem("")
        self.scan_time_combobox.addItem("")
        self.scan_time_combobox.addItem("")
        self.scan_time_combobox.addItem("")
        self.scan_time_combobox.addItem("")
        self.scan_time_combobox.addItem("")
        self.scan_time_combobox.addItem("")
        self.scan_time_combobox.addItem("")
        self.scan_time_combobox.addItem("")
        self.horizontalLayout.addWidget(self.scan_time_combobox)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.device_data_table = QtWidgets.QTableWidget(Form)
        self.device_data_table.setObjectName("device_data_table")
        self.device_data_table.setColumnCount(6)
        self.device_data_table.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.device_data_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.device_data_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.device_data_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.device_data_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.device_data_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.device_data_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.device_data_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.device_data_table.setHorizontalHeaderItem(5, item)
        self.device_data_table.horizontalHeader().setDefaultSectionSize(69)
        self.device_data_table.verticalHeader().setDefaultSectionSize(40)
        self.verticalLayout.addWidget(self.device_data_table)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_12 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 0, 0, 1, 3)
        self.dc_current_set_button = QtWidgets.QPushButton(Form)
        self.dc_current_set_button.setObjectName("dc_current_set_button")
        self.gridLayout.addWidget(self.dc_current_set_button, 2, 3, 1, 1)
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 4, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(Form)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 1, 1, 1, 1)
        self.dc_voltage_input = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dc_voltage_input.sizePolicy().hasHeightForWidth())
        self.dc_voltage_input.setSizePolicy(sizePolicy)
        self.dc_voltage_input.setObjectName("dc_voltage_input")
        self.gridLayout.addWidget(self.dc_voltage_input, 1, 2, 1, 1)
        self.dc_current_input = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dc_current_input.sizePolicy().hasHeightForWidth())
        self.dc_current_input.setSizePolicy(sizePolicy)
        self.dc_current_input.setObjectName("dc_current_input")
        self.gridLayout.addWidget(self.dc_current_input, 2, 2, 1, 1)
        self.eload_mode_set_button = QtWidgets.QPushButton(Form)
        self.eload_mode_set_button.setObjectName("eload_mode_set_button")
        self.gridLayout.addWidget(self.eload_mode_set_button, 5, 3, 1, 1)
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 5, 1, 1, 1)
        self.eload_mode_combobox = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eload_mode_combobox.sizePolicy().hasHeightForWidth())
        self.eload_mode_combobox.setSizePolicy(sizePolicy)
        self.eload_mode_combobox.setEditable(True)
        self.eload_mode_combobox.setObjectName("eload_mode_combobox")
        self.eload_mode_combobox.addItem("")
        self.eload_mode_combobox.addItem("")
        self.eload_mode_combobox.addItem("")
        self.eload_mode_combobox.addItem("")
        self.eload_mode_combobox.addItem("")
        self.gridLayout.addWidget(self.eload_mode_combobox, 4, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 4, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 2, 1, 1, 1)
        self.dc_voltage_set_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dc_voltage_set_button.sizePolicy().hasHeightForWidth())
        self.dc_voltage_set_button.setSizePolicy(sizePolicy)
        self.dc_voltage_set_button.setObjectName("dc_voltage_set_button")
        self.gridLayout.addWidget(self.dc_voltage_set_button, 1, 3, 1, 1)
        self.eload_mode_value_input = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eload_mode_value_input.sizePolicy().hasHeightForWidth())
        self.eload_mode_value_input.setSizePolicy(sizePolicy)
        self.eload_mode_value_input.setObjectName("eload_mode_value_input")
        self.gridLayout.addWidget(self.eload_mode_value_input, 5, 2, 1, 1)
        self.dc_output_on_button = QtWidgets.QPushButton(Form)
        self.dc_output_on_button.setObjectName("dc_output_on_button")
        self.gridLayout.addWidget(self.dc_output_on_button, 1, 4, 1, 1)
        self.dc_output_off_button = QtWidgets.QPushButton(Form)
        self.dc_output_off_button.setObjectName("dc_output_off_button")
        self.gridLayout.addWidget(self.dc_output_off_button, 2, 4, 1, 1)
        self.eload_input_on_button = QtWidgets.QPushButton(Form)
        self.eload_input_on_button.setObjectName("eload_input_on_button")
        self.gridLayout.addWidget(self.eload_input_on_button, 4, 4, 1, 1)
        self.eload_input_off_button = QtWidgets.QPushButton(Form)
        self.eload_input_off_button.setObjectName("eload_input_off_button")
        self.gridLayout.addWidget(self.eload_input_off_button, 5, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.setStretch(0, 8)
        self.verticalLayout.setStretch(3, 2)
        self.verticalLayout.setStretch(4, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 7)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 8)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.test_stop_button.setText(_translate("Form", "STOP"))
        self.test_start_button.setText(_translate("Form", "START"))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Test Contol:</span></p></body></html>"))
        item = self.test_status_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "Group"))
        item = self.test_status_table.verticalHeaderItem(1)
        item.setText(_translate("Form", "Group Cycle"))
        item = self.test_status_table.verticalHeaderItem(2)
        item.setText(_translate("Form", "Step"))
        item = self.test_status_table.verticalHeaderItem(3)
        item.setText(_translate("Form", "Action"))
        item = self.test_status_table.verticalHeaderItem(4)
        item.setText(_translate("Form", "Stop Judge"))
        item = self.test_status_table.verticalHeaderItem(5)
        item.setText(_translate("Form", "Limit Time"))
        item = self.test_status_table.verticalHeaderItem(6)
        item.setText(_translate("Form", "Wait Time"))
        item = self.test_status_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Value"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Device Data:</span></p></body></html>"))
        self.device_data_refresh_button.setText(_translate("Form", "Refresh"))
        self.device_data_scan_checkbox.setText(_translate("Form", "Scan"))
        self.scan_time_combobox.setCurrentText(_translate("Form", "1"))
        self.scan_time_combobox.setItemText(0, _translate("Form", "1"))
        self.scan_time_combobox.setItemText(1, _translate("Form", "2"))
        self.scan_time_combobox.setItemText(2, _translate("Form", "3"))
        self.scan_time_combobox.setItemText(3, _translate("Form", "4"))
        self.scan_time_combobox.setItemText(4, _translate("Form", "5"))
        self.scan_time_combobox.setItemText(5, _translate("Form", "6"))
        self.scan_time_combobox.setItemText(6, _translate("Form", "7"))
        self.scan_time_combobox.setItemText(7, _translate("Form", "8"))
        self.scan_time_combobox.setItemText(8, _translate("Form", "9"))
        item = self.device_data_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "DC"))
        item = self.device_data_table.verticalHeaderItem(1)
        item.setText(_translate("Form", "Eload"))
        item = self.device_data_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "State"))
        item = self.device_data_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Mode"))
        item = self.device_data_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Setting"))
        item = self.device_data_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Voltage"))
        item = self.device_data_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Current"))
        item = self.device_data_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Power"))
        self.label_12.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">DC / ELoad控制</span></p></body></html>"))
        self.dc_current_set_button.setText(_translate("Form", "Set"))
        self.label_15.setText(_translate("Form", "<html><head/><body><p align=\"center\">模式</p></body></html>"))
        self.label_13.setText(_translate("Form", "<html><head/><body><p align=\"center\">电压</p></body></html>"))
        self.eload_mode_set_button.setText(_translate("Form", "Set"))
        self.label_11.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">DC</span></p></body></html>"))
        self.label_16.setText(_translate("Form", "<html><head/><body><p align=\"center\">数值</p></body></html>"))
        self.eload_mode_combobox.setItemText(0, _translate("Form", "CC"))
        self.eload_mode_combobox.setItemText(1, _translate("Form", "CP"))
        self.eload_mode_combobox.setItemText(2, _translate("Form", "CR"))
        self.eload_mode_combobox.setItemText(3, _translate("Form", "TCC"))
        self.eload_mode_combobox.setItemText(4, _translate("Form", "TCP"))
        self.label_10.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Eload</span></p></body></html>"))
        self.label_14.setText(_translate("Form", "<html><head/><body><p align=\"center\">电流</p></body></html>"))
        self.dc_voltage_set_button.setText(_translate("Form", "Set"))
        self.dc_output_on_button.setText(_translate("Form", "输出 ON"))
        self.dc_output_off_button.setText(_translate("Form", "输出 OFF"))
        self.eload_input_on_button.setText(_translate("Form", "输入 ON"))
        self.eload_input_off_button.setText(_translate("Form", "输入 OFF"))
