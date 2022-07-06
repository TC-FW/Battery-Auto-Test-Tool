import re
import threading
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView

from homepage import ui_main_tab


class MainTab(QMainWindow, ui_main_tab.Ui_Form):
    input_register_name_signal= QtCore.pyqtSignal(str)
    input_register_value_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent, tab):
        super(MainTab, self).__init__(parent)
        self.setupUi(tab)
        self.input_register_name_signal.connect(self.table_register_name_update)
        self.input_register_value_signal.connect(self.table_register_value_update)

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
