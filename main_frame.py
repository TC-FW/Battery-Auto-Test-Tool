import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore

import homepage.ui_main_tab
import rule_tab
from homepage import ui_mainwindow

'''class MyComboBox(QtWidgets.QComboBox):
    clicked = QtCore.pyqtSignal()  # 创建一个信号

    def showPopup(self):  # 重写showPopup函数
        self.clicked.emit()  # 发送信号        
        super(MyComboBox, self).showPopup()   # 调用父类的showPopup()'''


class MyMainForm(QMainWindow, ui_mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("VPD Toolbox V1.0")
        self.tab1 = homepage.ui_main_tab.Ui_Form.setupUi(self,self.window_tab_1)
        self.tab2 = rule_tab.RuleTab(self, self.window_tab_2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
