import re

from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QHeaderView, QCheckBox

from homepage import ui_main_tab


class MainTab(QMainWindow, ui_main_tab.Ui_Form):
    input_register_name_signal= QtCore.pyqtSignal(str)
    input_register_value_signal = QtCore.pyqtSignal(str)
    input_test_status_signal = QtCore.pyqtSignal(bool)
    input_test_status_table_signal = QtCore.pyqtSignal(int, str, bool)
    input_monitor_register_signal = QtCore.pyqtSignal(str, str)

    output_test_start_signal = QtCore.pyqtSignal()
    output_test_stop_signal = QtCore.pyqtSignal()
    output_device_scan_signal = QtCore.pyqtSignal(bool)
    output_dc_control_signal = QtCore.pyqtSignal(str, str)
    output_eload_control_signal = QtCore.pyqtSignal(str, str)
    output_monitor_register_num_signal = QtCore.pyqtSignal(bool, int)

    def __init__(self, parent, tab):
        super(MainTab, self).__init__(parent)
        self.setupUi(tab)

        self.test_start_button.setEnabled(True)
        self.test_stop_button.setEnabled(False)

        self.input_register_name_signal.connect(self.table_register_name_update)
        self.input_register_value_signal.connect(self.table_register_value_update)
        self.input_test_status_signal.connect(self.test_status_update)
        self.input_test_status_table_signal.connect(self.test_status_table_update)
        self.input_monitor_register_signal.connect(self.moniter_register_update)

        self.test_start_button.clicked.connect(lambda: self.output_test_start_signal.emit())
        self.test_stop_button.clicked.connect(lambda: self.output_test_stop_signal.emit())

        self.device_data_scan_checkbox.clicked.connect(
            lambda: self.output_device_scan_signal.emit(True) if self.device_data_scan_checkbox.isChecked()
            else self.output_device_scan_signal.emit(False))

        self.test_status_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.register_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.register_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.device_data_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.device_data_table.setSelectionMode(QAbstractItemView.NoSelection)

        self.device_data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.device_data_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.test_status_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.test_status_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.register_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.monitor_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # DC控制信号
        self.dc_voltage_set_button.clicked.connect(
            lambda: self.output_dc_control_signal.emit('voltage', self.dc_voltage_input.text()))
        self.dc_current_set_button.clicked.connect(
            lambda: self.output_dc_control_signal.emit('current', self.dc_current_input.text()))
        self.dc_output_on_button.clicked.connect(
            lambda: self.output_dc_control_signal.emit('output', 'on'))
        self.dc_output_off_button.clicked.connect(
            lambda: self.output_dc_control_signal.emit('output', 'off'))
        self.dc_voltage_input.returnPressed.connect(lambda: self.dc_voltage_set_button.click())
        self.dc_current_input.returnPressed.connect(lambda: self.dc_current_set_button.click())
        # Eload控制信号
        self.eload_mode_set_button.clicked.connect(
            lambda: self.output_eload_control_signal.emit(self.eload_mode_combobox.currentText(),
                                                          self.eload_mode_value_input.text()))
        self.eload_input_on_button.clicked.connect(
            lambda: self.output_eload_control_signal.emit('input', 'on'))
        self.eload_input_off_button.clicked.connect(
            lambda: self.output_eload_control_signal.emit('input', 'off'))
        self.eload_mode_value_input.returnPressed.connect(lambda : self.eload_mode_set_button.click())

        self.register_table.doubleClicked.connect(self.add_monitor_register)

    def table_register_name_update(self, register_name_line):
        register_name = re.split(';|,|\t|\n', register_name_line)
        self.register_table.clear() # 清空表格
        self.register_table.setColumnCount(3)  # 设定列数
        self.register_table.setRowCount(len(register_name))  # 设定行数
        self.register_table.setHorizontalHeaderLabels(['Register', 'Value', 'Monitor'])  # 设定列的标题

        for i in range(len(register_name)):
            self.register_table.setItem(i, 0, QTableWidgetItem(register_name[i]))
            self.register_table.setItem(i, 2, QTableWidgetItem('Double click to monitor'))
            self.register_table.item(i, 2).setForeground(QBrush(QColor('light grey')))
        self.register_table.update()

    def table_register_value_update(self, register_value_line):
        register_value = re.split(';|,|\t|\n', register_value_line)
        for i in range(len(register_value)):
            self.register_table.setItem(i, 1, QTableWidgetItem(register_value[i]))
        self.register_table.update()

    def moniter_register_update(self, register_name_line, register_value_line):
        if register_name_line == '' or register_value_line == '':
            return
        register_name = re.split(';|,|\t|\n', register_name_line)
        register_value = re.split(';|,|\t|\n', register_value_line)
        self.monitor_table.clear()  # 清空表格
        self.monitor_table.setColumnCount(2)  # 设定列数
        self.monitor_table.setRowCount(len(register_name))  # 设定行数
        self.monitor_table.setHorizontalHeaderLabels(['Register', 'Value'])  # 设定列的标题

        for i in range(len(register_name)):
            if register_name[i] != '' and register_value[i] != '':
                self.monitor_table.setItem(i, 0, QTableWidgetItem(register_name[i]))
                self.monitor_table.setItem(i, 1, QTableWidgetItem(register_value[i]))
        self.monitor_table.update()

    def add_monitor_register(self, item):
        if item.column() == 2:
            if item.data() == 'Double click to monitor':
                self.register_table.setItem(item.row(), item.column(), QTableWidgetItem('Monitoring'))
                self.register_table.item(item.row(), item.column()).setForeground(QBrush(QColor('blue')))
                self.output_monitor_register_num_signal.emit(True, item.row())
            elif item.data() == 'Monitoring':
                self.register_table.setItem(item.row(), item.column(), QTableWidgetItem('Double click to monitor'))
                self.register_table.item(item.row(), item.column()).setForeground(QBrush(QColor('light grey')))
                self.output_monitor_register_num_signal.emit(False, item.row())

    def test_status_update(self, status):
        if status:
            self.test_start_button.setEnabled(False)
            self.test_stop_button.setEnabled(True)
        else:
            self.test_start_button.setEnabled(True)
            self.test_stop_button.setEnabled(False)

    def test_status_table_update(self, row, string, clear):
        if clear:
            self.test_status_table.clearContents()
        self.test_status_table.setItem(row, 0, QTableWidgetItem(string))
