import os
import re
import sys
import threading
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore

import main_tab
import rule_tab
from homepage import ui_mainwindow

'''class MyComboBox(QtWidgets.QComboBox):
    clicked = QtCore.pyqtSignal()  # 创建一个信号

    def showPopup(self):  # 重写showPopup函数
        self.clicked.emit()  # 发送信号        
        super(MyComboBox, self).showPopup()   # 调用父类的showPopup()'''


class MyMainForm(QMainWindow, ui_mainwindow.Ui_MainWindow):
    input_rule_signal = QtCore.pyqtSignal(str, str, str, str)
    output_register_name_signal = QtCore.pyqtSignal(str)
    output_register_value_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.register_line = None
        self.group_loop_count = None
        self.log_file_path = ''
        self.cycle_rule = None
        self.setupUi(self)
        self.setWindowTitle("VPD Toolbox V1.0")
        self.tab1 = main_tab.MainTab(self, self.window_tab_1)
        self.tab2 = rule_tab.RuleTab(self, self.window_tab_2)

        self.tab2.output_rule_signal.connect(self.input_rule_signal)

        self.output_register_name_signal.connect(self.tab1.input_register_name_signal)
        self.output_register_value_signal.connect(self.tab1.input_register_value_signal)

        self.input_rule_signal.connect(self.rule_process)
        self.tab1.test_start_button.clicked.connect(self.test_thread)

    def rule_process(self, log_path, log_first_value, cycle_rule, group_loop_count):
        # 检查Log文件路径
        if not os.path.exists(log_path):
            QMessageBox.warning(self, 'Warning', 'Log文件不存在，请检查文件路径是否正确。')
            return

        # 检查数据开始段落
        file = open(log_path, 'r')
        begin_line = 0
        while True:
            line = file.readline()
            if line != '':
                if log_first_value == re.split(';|,|\t|\n', line)[0]:
                    break
                else:
                    begin_line += 1
            else:
                QMessageBox.warning(self, 'Warning', 'Log文件中未发现以\'%s\'开头的段落，请检查输入是否正确。' % log_first_value)
                return

        temp_rule = cycle_rule.split(';')
        temp_cycle_rule = []
        for i in temp_rule:
            if i != '':
                temp_cycle_rule.append(i.split(','))

        for i in temp_cycle_rule:
            if i[3] not in re.split(';|,|\t|\n', line):
                QMessageBox.warning(self, 'Warning', 'Log文件中未找到\'%s\'，请检查输入是否正确' % i[3])
                return

        for i in re.split(';| |,|\t|\n', group_loop_count):
            if i.isdigit() or i == '':
                pass
            else:
                QMessageBox.warning(self, 'Warning', 'Group循环次数只能输入分隔符和数字')

        self.output_register_name_signal.emit(line)

        self.log_file_path = log_path
        self.cycle_rule = temp_cycle_rule
        self.register_line = re.split(';|,|\t|\n', line)
        self.group_loop_count = re.split(';| |,|\t|\n', group_loop_count)

    def test_thread(self):
        test = threading.Thread(target=self.log_line_update, daemon=True)
        test.start()

    def log_line_update(self):
        log_file = open(self.log_file_path, 'rb')
        line = []
        while True:
            offset = -100
            while True:
                try:
                    log_file.seek(offset, 2)
                    line = log_file.readlines()
                    if len(line) >= 2 and '\n' in line[-1].decode('utf-8'):
                        break
                    else:
                        offset *= 2
                        time.sleep(0.3)
                except:
                    time.sleep(0.3)
                    continue

            self.output_register_value_signal.emit(line[-1].decode('utf-8'))
            time.sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
