import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QCheckBox, QHeaderView

from homepage import rule_tab


class MyMainForm(QMainWindow, rule_tab.Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.pushButton.clicked.connect(self.display)
        self.pushButton_2.clicked.connect(self.add_rule)
        self.pushButton_3.clicked.connect(self.del_rule)

    def add_rule(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
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

        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 0, checkbox)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 2, comBox1)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 4, comBox2)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 6, comBox3)

    def del_rule(self):
        if self.tableWidget.rowCount() > 0:
            self.tableWidget.setRowCount(self.tableWidget.rowCount() - 1)

    def display(self):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                if j == 0:
                    print(self.tableWidget.cellWidget(i, j).isChecked(), end=', ')
                elif j == 2 or j == 4 or j == 6:
                    print(self.tableWidget.cellWidget(i, j).currentText(), end=', ')
                elif self.tableWidget.item(i, j) is not None:
                    print(self.tableWidget.item(i, j).text(), end=', ')
                else:
                    print(None, end=', ')
            print()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
