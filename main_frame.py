import os
import re
import sys
import threading
import time

import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore
import serial.tools.list_ports

import judge
import main_tab
import rule_tab
import serial_control_tab
from homepage import ui_mainwindow
import dc_control
import eload_control


'''class MyComboBox(QtWidgets.QComboBox):
    clicked = QtCore.pyqtSignal()  # 创建一个信号

    def showPopup(self):  # 重写showPopup函数
        self.clicked.emit()  # 发送信号        
        super(MyComboBox, self).showPopup()   # 调用父类的showPopup()'''


class MyMainForm(QMainWindow, ui_mainwindow.Ui_MainWindow):
    input_rule_signal = QtCore.pyqtSignal(str, str, str, str)
    input_test_start_signal = QtCore.pyqtSignal()
    input_test_stop_signal = QtCore.pyqtSignal()
    input_serial_scan_signal = QtCore.pyqtSignal(str)
    input_serial_connect_signal = QtCore.pyqtSignal(str, str)
    input_dc_control_signal = QtCore.pyqtSignal(str, str)
    input_eload_control_signal = QtCore.pyqtSignal(str, str)

    output_register_name_signal = QtCore.pyqtSignal(str)
    output_register_value_signal = QtCore.pyqtSignal(str)
    output_test_status_signal = QtCore.pyqtSignal(bool)
    output_test_status_table_signal = QtCore.pyqtSignal(int, str, bool)
    output_serial_list_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.register_data = []
        self.register_line = []
        self.group_loop_count = []
        self.log_file_path = ''
        self.cycle_rule = None

        self.setupUi(self)
        self.setWindowTitle("Battery Auto Testing Tool Beta V1.0")
        self.main_tab = main_tab.MainTab(self, self.window_tab_1)
        self.rule_tab = rule_tab.RuleTab(self, self.window_tab_2)
        self.serial_control_tab = serial_control_tab.SerialControlTab(self, self.window_tab_3)

        self.dc_device = dc_control.HengHuiDC()
        self.eload_device = eload_control.HengHuiEload()

        self.test_status = False

        self.main_tab.output_test_start_signal.connect(self.input_test_start_signal)
        self.main_tab.output_test_stop_signal.connect(self.input_test_stop_signal)
        self.rule_tab.output_rule_signal.connect(self.input_rule_signal)
        self.serial_control_tab.output_serial_scan_signal.connect(self.input_serial_scan_signal)
        self.serial_control_tab.output_serial_connect_signal.connect(self.input_serial_connect_signal)
        self.serial_control_tab.output_dc_control_signal.connect(self.input_dc_control_signal)
        self.serial_control_tab.output_eload_control_signal.connect(self.input_eload_control_signal)

        self.output_register_name_signal.connect(self.main_tab.input_register_name_signal)
        self.output_register_value_signal.connect(self.main_tab.input_register_value_signal)
        self.output_test_status_signal.connect(self.main_tab.input_test_status_signal)
        self.output_test_status_table_signal.connect(self.main_tab.input_test_status_table_signal)
        self.output_serial_list_signal.connect(self.serial_control_tab.input_serial_list_signal)

        self.input_rule_signal.connect(self.rule_process)
        self.input_test_start_signal.connect(self.test_start_thread)
        self.input_test_stop_signal.connect(self.test_stop)
        self.input_serial_scan_signal.connect(self.serial_device_scan)
        self.input_serial_connect_signal.connect(self.serial_serial_connect)
        self.input_dc_control_signal.connect(self.dc_control)
        self.input_eload_control_signal.connect(self.eload_control)

    def serial_device_scan(self, device):
        """
        扫描电脑上的串口设备
        """
        return_device_list = ''
        serial_device_list = serial.tools.list_ports.comports()
        for i in serial_device_list:
            return_device_list += i[0] + ' #' + i[1] + ','
        self.output_serial_list_signal.emit(device, return_device_list[:-1])

    def serial_serial_connect(self, dc_serial_config, eload_serial_config):
        dc_config = dc_serial_config.split(',')
        eload_config = eload_serial_config.split(',')
        if dc_config[0] != '' and dc_config[1] != '':
            self.dc_device.serial_disconnect()
            self.dc_device.device_connect(dc_config[0], dc_config[1], stopbits=2)
        else:
            QMessageBox.warning(self, 'warning', '请检查DC参数是否填写完全')

        if eload_config[0] != '' and eload_config[1] != '':
            self.eload_device.serial_disconnect()
            self.eload_device.device_connect(eload_config[0], eload_config[1], stopbits=2)
        else:
            QMessageBox.warning(self, 'warning', '请检查ELoad参数是否填写完全')

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

        QMessageBox.information(self, 'Success', '保存成功')

    def test_start_thread(self):
        if not self.log_file_path or not self.register_line:
            QMessageBox.warning(self, 'Warning', '请先切换到"规则设定"页面，按OK键保存设置。')
            return False
        self.test_status = True
        log_data_update = threading.Thread(target=self.log_data_update, daemon=True)
        log_data_update.start()

        test_step = threading.Thread(target=self.test_step, daemon=True)
        test_step.start()

        self.output_test_status_signal.emit(True)

    def test_stop(self):
        self.test_status = False
        self.output_test_status_signal.emit(False)

    def log_data_update(self):
        log_file = open(self.log_file_path, 'rb')
        line = []
        while self.test_status:
            offset = -100
            while self.test_status:
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
            if self.test_status:
                self.register_data = re.split(';|,|\t|\n', line[-1].decode('utf-8'))

                self.output_register_value_signal.emit(line[-1].decode('utf-8'))
                time.sleep(0.3)

    def test_step(self):
        step_num = 0
        group_current_num = ''
        group_current_cycle_count = 1

        while self.test_status:
            if self.cycle_rule[step_num][0] == 'True':
                if self.cycle_rule[step_num][1] == group_current_num:
                    # 更新主页面table中的group编号和group循环计数
                    if group_current_num != '':
                        self.output_test_status_table_signal.emit(0, str(group_current_num), True)
                        self.output_test_status_table_signal.emit(1, '%s/%s' % (
                            group_current_cycle_count, self.group_loop_count[int(group_current_num) - 1]), False)
                    else:
                        self.output_test_status_table_signal.emit(0, '', True)
                        self.output_test_status_table_signal.emit(1, '', False)
                    self.output_test_status_table_signal.emit(2, str(step_num + 1), False)
                    self.output_test_status_table_signal.emit(3, self.cycle_rule[step_num][2], False)

                    '''ACTION START CODE'''  # 等待添加
                    # 等待停止条件触发
                    limit_time_begin = time.time()
                    while self.test_status:
                        if len(self.register_data) == len(self.register_line):
                            temp_register_value = self.register_data[
                                self.register_line.index(self.cycle_rule[step_num][3])]
                            if temp_register_value != '' and judge.judge(temp_register_value, self.cycle_rule[step_num][5], self.cycle_rule[step_num][4]):
                                self.output_test_status_table_signal.emit(4, '%s %s %s 停止条件触发' % (
                                    temp_register_value, self.cycle_rule[step_num][4], self.cycle_rule[step_num][5]), False)
                                break
                            else:
                                self.output_test_status_table_signal.emit(4, '%s %s %s 未满足停止条件' % (
                                    temp_register_value, self.cycle_rule[step_num][4], self.cycle_rule[step_num][5]), False)
                        else:
                            self.output_test_status_table_signal.emit(4, '%s %s %s 未满足停止条件' % (
                                '', self.cycle_rule[step_num][4], self.cycle_rule[step_num][5]), False)
                        time.sleep(0.1)

                    '''ACTION STOP CODE'''  # 等待添加

                    # 等待阶段
                    begin_wait_time = time.time()
                    while self.cycle_rule[step_num][6] != '' and self.test_status:
                        current_wait_time = time.time() - begin_wait_time
                        self.output_test_status_table_signal.emit(5, '%s / %s' % (
                            current_wait_time, self.cycle_rule[step_num][6]), False)
                        if current_wait_time >= int(self.cycle_rule[step_num][6]):
                            break
                        time.sleep(0.1)

                    if self.test_status:
                        step_num += 1
                        if step_num > len(self.cycle_rule) - 1:  # step计数溢出处理
                            # 1.若该步骤未分组，直接结束测试
                            # 2.若循环组已完成循环次数，结束测试
                            if (self.cycle_rule[step_num - 1][1] == '' or
                                    group_current_cycle_count >= int(self.group_loop_count[int(group_current_num) - 1])):
                                print('Group%s循环%s' % (group_current_num, group_current_cycle_count))
                                print('Group%s完成' % group_current_num)
                                break
                            # 如果循环组为完成循环次数，step_num取余继续继续测试
                            elif group_current_cycle_count < int(self.group_loop_count[int(group_current_num) - 1]):
                                print('Group%s循环%s' % (group_current_num, group_current_cycle_count))
                                group_current_cycle_count += 1
                                step_num = step_num % len(self.cycle_rule)

                        else:  # step计数未溢出
                            # 1. 判断该step是否有Group编号
                            # 2. 判断该Group循环是否完成
                            if self.cycle_rule[step_num][1] != group_current_num:
                                if (group_current_num != '' and
                                        group_current_cycle_count < int(self.group_loop_count[int(group_current_num) - 1])):
                                    print('Group%s循环%s' % (group_current_num, group_current_cycle_count))
                                    group_current_cycle_count += 1
                                else:
                                    print('Group%s循环%s' % (group_current_num, group_current_cycle_count))
                                    print('Group%s完成' % group_current_num)
                                    group_current_num = self.cycle_rule[step_num][1]
                                    group_current_cycle_count = 1

                elif group_current_num == '':
                    group_current_num = self.cycle_rule[step_num][1]
                else:
                    step_num = (step_num + 1) % len(self.cycle_rule)
            else:
                step_num += 1

            if step_num > len(self.cycle_rule) - 1:
                break

        self.test_stop()
        print('test stop')

    def dc_control(self, config, value):
        if self.dc_device.connect_flag:
            if config == 'current':
                self.dc_device.set_current(value)
            elif config == 'voltage':
                self.dc_device.set_voltage(value)
            elif config == 'output' and value == 'on':
                self.dc_device.output_on()
            elif config == 'output' and value == 'off':
                self.dc_device.output_off()

    def eload_control(self, config, value):
        if self.eload_device.connect_flag:
            if config == 'CC':
                self.eload_device.set_cc_mode(value)
            elif config == 'CP':
                self.eload_device.set_cp_mode(value)
            elif config == 'CR':
                self.eload_device.set_cr_mode(value)
            elif config == 'TCC':
                tcc_setting = re.split('@|,|;', value)
                self.eload_device.set_tran_cc_mode(tcc_setting[0], tcc_setting[1], tcc_setting[2], tcc_setting[3])
            elif config == 'input' and value == 'on':
                self.eload_device.input_on()
            elif config == 'input' and value == 'off':
                self.eload_device.input_off()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
