import os

from PyQt5.QtWidgets import QMainWindow, QComboBox, QCheckBox, QHeaderView, QFileDialog

from homepage import ui_rule_tab


class RuleTab(QMainWindow, ui_rule_tab.Ui_Form):
    def __init__(self, parent, tab):
        super(RuleTab, self).__init__(parent)
        self.setupUi(tab)
        self.rule_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.enter_button.clicked.connect(self.display)
        self.add_rule_button.clicked.connect(self.add_rule)
        self.del_rule_button.clicked.connect(self.del_rule)
        self.log_select_button.clicked.connect(self.log_file_select)

    def add_rule(self):
        self.rule_table.setRowCount(self.rule_table.rowCount() + 1)
        comBox1 = QComboBox()
        comBox1.addItems(['Charge', 'Discharge', 'None'])
        comBox1.setEditable(True)

        checkbox = QCheckBox()
        checkbox.setChecked(True)

        comBox2 = QComboBox()
        comBox2.addItems(['>', '<', '=', '>=', '<=', 'Set', 'Reset'])
        comBox2.setEditable(True)

        comBox3 = QComboBox()
        comBox3.addItems(['>', '<', '=', '>=', '<=', 'Set', 'Reset'])
        comBox3.setEditable(True)

        self.rule_table.setCellWidget(self.rule_table.rowCount() - 1, 0, checkbox)
        self.rule_table.setCellWidget(self.rule_table.rowCount() - 1, 2, comBox1)
        self.rule_table.setCellWidget(self.rule_table.rowCount() - 1, 4, comBox2)
        self.rule_table.setCellWidget(self.rule_table.rowCount() - 1, 7, comBox3)

    def del_rule(self):
        if self.rule_table.rowCount() > 0:
            self.rule_table.setRowCount(self.rule_table.rowCount() - 1)

    def display(self):
        for i in range(self.rule_table.rowCount()):
            for j in range(self.rule_table.columnCount()):
                if j == 0:
                    print(self.rule_table.cellWidget(i, j).isChecked(), end=', ')
                elif j == 2 or j == 4 or j == 7:
                    print(self.rule_table.cellWidget(i, j).currentText(), end=', ')
                elif self.rule_table.item(i, j) is not None:
                    print(self.rule_table.item(i, j).text(), end=', ')
                else:
                    print(None, end=', ')
            print()

    def log_file_select(self):
        """
        导出文件夹选择
        :return: None
        """
        file_name = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),"Log Files(*.log);;All Files(*)")
        if file_name[0]:
            self.file_select_input.setText(file_name[0])
