import re
import threading
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView

from homepage import ui_main_tab


class MainTab(QMainWindow, ui_main_tab.Ui_Form):
    input_register_name_signal= QtCore.pyqtSignal(str)
    input_register_value_signal = QtCore.pyqtSignal(str)
    input_test_status_signal = QtCore.pyqtSignal(bool)
    input_test_status_table_signal = QtCore.pyqtSignal(int, str, bool)

    output_test_start_signal = QtCore.pyqtSignal()
    output_test_stop_signal = QtCore.pyqtSignal()

    def __init__(self, parent, tab):
        super(MainTab, self).__init__(parent)
        self.setupUi(tab)

        self.test_start_button.setEnabled(True)
        self.test_stop_button.setEnabled(False)

        self.input_register_name_signal.connect(self.table_register_name_update)
        self.input_register_value_signal.connect(self.table_register_value_update)
        self.input_test_status_signal.connect(self.test_status_update)
        self.input_test_status_table_signal.connect(self.test_status_table_update)

        self.test_start_button.clicked.connect(lambda: self.output_test_start_signal.emit())
        self.test_stop_button.clicked.connect(lambda: self.output_test_stop_signal.emit())

    def table_register_name_update(self, register_name_line):
        register_name = re.split(';|,|\t|\n', register_name_line)
        self.register_table.clear()  # 清空表格
        self.register_table.setColumnCount(2)  # 设定列数
        self.register_table.setRowCount(len(register_name))  # 设定行数
        self.register_table.setHorizontalHeaderLabels(['Register', 'Value'])  # 设定列的标题
        for i in range(len(register_name)):
            self.register_table.setItem(i, 0, QTableWidgetItem(register_name[i]))
        self.register_table.update()

    def table_register_value_update(self, register_value_line):
        register_value = re.split(';|,|\t|\n', register_value_line)
        for i in range(len(register_value)):
            self.register_table.setItem(i, 1, QTableWidgetItem(register_value[i]))
        self.register_table.update()

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
