import os
import re

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QComboBox, QCheckBox, QHeaderView, QFileDialog, QMessageBox

from homepage import ui_rule_tab


class RuleTab(QMainWindow, ui_rule_tab.Ui_Form):
    output_rule_signal = QtCore.pyqtSignal(str, str, str, str)

    def __init__(self, parent, tab):
        super(RuleTab, self).__init__(parent)
        self.setupUi(tab)
        self.rule_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.enter_button.clicked.connect(self.display)
        self.add_rule_button.clicked.connect(self.add_rule)
        self.del_rule_button.clicked.connect(self.del_rule)
        self.log_select_button.clicked.connect(self.log_file_select)

        self.register_list = []

        self.file_select_input.textChanged.connect(self.register_list_update)
        self.log_first_value_combox.currentTextChanged.connect(self.register_list_update)

    def add_rule(self):
        self.rule_table.setRowCount(self.rule_table.rowCount() + 1)
        comBox1 = QComboBox()
        comBox1.addItems(['Charge', 'Discharge', 'None'])
        comBox1.setEditable(True)

        checkbox = QCheckBox()
        checkbox.setChecked(True)

        register_combox = QComboBox()
        register_combox.addItems(self.register_list)
        register_combox.setEditable(True)

        comBox2 = QComboBox()
        comBox2.addItems(['>', '<', '=', '>=', '<=', 'Set', 'Reset'])
        comBox2.setEditable(True)

        self.rule_table.setCellWidget(self.rule_table.rowCount() - 1, 0, checkbox)
        self.rule_table.setCellWidget(self.rule_table.rowCount() - 1, 2, comBox1)
        self.rule_table.setCellWidget(self.rule_table.rowCount() - 1, 3, register_combox)
        self.rule_table.setCellWidget(self.rule_table.rowCount() - 1, 4, comBox2)

    def del_rule(self):
        if self.rule_table.rowCount() > 0:
            self.rule_table.setRowCount(self.rule_table.rowCount() - 1)

    def display(self):
        temp_rule = ''
        for i in range(self.rule_table.rowCount()):
            for j in range(self.rule_table.columnCount()):
                if j == 0:
                    temp_rule += str(self.rule_table.cellWidget(i, j).isChecked()) + ','
                elif j == 2 or j == 3 or j == 4:
                    temp_rule += str(self.rule_table.cellWidget(i, j).currentText()) + ','
                elif self.rule_table.item(i, j) is not None:
                    temp_rule += self.rule_table.item(i, j).text() + ','
                else:
                    temp_rule += '' + ','
                if j == self.rule_table.columnCount() - 1:
                    temp_rule = temp_rule[:-1] + ';'

        self.output_rule_signal.emit(self.file_select_input.text(), self.log_first_value_combox.currentText(),
                                     temp_rule, self.group_cycle_count_input.text())
        return True

    def log_file_select(self):
        """
        导出文件夹选择
        :return: None
        """
        file_name = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "Log Files(*.log;*.csv);;All Files(*)")
        if file_name[0]:
            self.file_select_input.setText(file_name[0])
            if file_name[0][-4:] == '.log':
                self.log_first_value_combox.setCurrentText('Sample')
            elif file_name[0][-4:] == '.csv':
                self.log_first_value_combox.setCurrentText('Time')

    def register_list_update(self):
        if not os.path.exists(self.file_select_input.text()):
            return

        file = open(self.file_select_input.text(), 'r')
        begin_line = 0
        while True:
            line = file.readline()
            if begin_line <= 100:
                if self.log_first_value_combox.currentText() == re.split(';|,|\t|\n', line)[0]:
                    break
                else:
                    begin_line += 1
            else:
                return False

        self.register_list = re.split(';|,|\t|\n', line)
