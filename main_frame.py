import os
import re
import sys
import threading
import time
import serial
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStyleFactory

import serial.tools.list_ports

import judge
import main_tab
import rule_tab
import serial_control_tab
from homepage import ui_mainwindow
import dc_control
import eload_control

'''class MyComboBox(QtWidgets.QComboBox):
    clicked = pyqtSignal()  # 创建一个信号

    def showPopup(self):  # 重写showPopup函数
        self.clicked.emit()  # 发送信号        
        super(MyComboBox, self).showPopup()   # 调用父类的showPopup()'''


class MyMainForm(QMainWindow, ui_mainwindow.Ui_MainWindow):
    input_rule_signal = QtCore.pyqtSignal(str, str, str, str, str)
    input_test_start_signal = QtCore.pyqtSignal()
    input_test_stop_signal = QtCore.pyqtSignal()
    input_serial_scan_signal = QtCore.pyqtSignal(str)
    input_serial_connect_signal = QtCore.pyqtSignal(str, str)
    input_serial_disconnect_signal = QtCore.pyqtSignal()
    input_dc_control_signal = QtCore.pyqtSignal(str, str)
    input_eload_control_signal = QtCore.pyqtSignal(str, str)
    input_device_data_scan_signal = QtCore.pyqtSignal(bool)
    input_device_data_scan_time_signal = QtCore.pyqtSignal(str)
    input_device_data_refresh_signal = QtCore.pyqtSignal()
    input_monitor_register_num_signal = QtCore.pyqtSignal(bool, int)

    output_register_name_signal = QtCore.pyqtSignal(str)
    output_register_value_signal = QtCore.pyqtSignal(str)
    output_test_status_signal = QtCore.pyqtSignal(bool)
    output_test_status_table_signal = QtCore.pyqtSignal(int, str, bool)
    output_serial_list_signal = QtCore.pyqtSignal(str, str)
    output_monitor_register_signal = QtCore.pyqtSignal(str, str)
    output_device_data_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.register_data = []
        self.register_line = []
        self.group_loop_count = []
        self.monitor_register_list = []
        self.log_file_path = ''
        self.cycle_rule = None
        self.device_init_flag = True

        self.dc_init_mode = False
        self.dc_init_current = ''
        self.dc_init_voltage = ''

        self.setupUi(self)
        self.setWindowTitle("Battery Auto Testing Tool V2.0")
        self.main_tab = main_tab.MainTab(self, self.window_tab_1)
        self.rule_tab = rule_tab.RuleTab(self, self.window_tab_2)
        self.serial_control_tab = serial_control_tab.SerialControlTab(self, self.window_tab_3)

        self.dc_device = dc_control.HengHuiDC()
        self.eload_device = eload_control.HengHuiEload()

        self.device_data_scan_flag = False
        self.dc_data_refresh_flag = False
        self.eload_data_refresh_flag = False
        self.device_data_scan_time = 5
        self.dc_data_scan_thread = threading.Thread
        self.eload_data_scan_thread = threading.Thread

        self.test_status = False
        self.log_data_update_thread = threading.Thread
        self.test_step_thread = threading.Thread

        self.main_tab.output_test_start_signal.connect(self.input_test_start_signal)
        self.main_tab.output_test_stop_signal.connect(self.input_test_stop_signal)
        self.main_tab.output_device_data_scan_signal.connect(self.input_device_data_scan_signal)
        self.main_tab.output_device_data_scan_time_signal.connect(self.input_device_data_scan_time_signal)
        self.main_tab.output_device_data_refresh_signal.connect(self.device_data_refresh)
        self.main_tab.output_dc_control_signal.connect(self.input_dc_control_signal)
        self.main_tab.output_eload_control_signal.connect(self.input_eload_control_signal)
        self.main_tab.output_monitor_register_num_signal.connect(self.input_monitor_register_num_signal)
        self.rule_tab.output_rule_signal.connect(self.input_rule_signal)
        self.serial_control_tab.output_serial_scan_signal.connect(self.input_serial_scan_signal)
        self.serial_control_tab.output_serial_connect_signal.connect(self.input_serial_connect_signal)
        self.serial_control_tab.output_serial_disconnect_signal.connect(self.input_serial_disconnect_signal)
        self.serial_control_tab.output_dc_control_signal.connect(self.input_dc_control_signal)
        self.serial_control_tab.output_eload_control_signal.connect(self.input_eload_control_signal)

        self.output_register_name_signal.connect(self.main_tab.input_register_name_signal)
        self.output_register_value_signal.connect(self.main_tab.input_register_value_signal)
        self.output_test_status_signal.connect(self.main_tab.input_test_status_signal)
        self.output_test_status_table_signal.connect(self.main_tab.input_test_status_table_signal)
        self.output_monitor_register_signal.connect(self.main_tab.input_monitor_register_signal)
        self.output_device_data_signal.connect(self.main_tab.input_device_data_signal)
        self.output_serial_list_signal.connect(self.serial_control_tab.input_serial_list_signal)

        self.input_rule_signal.connect(self.rule_process)
        self.input_test_start_signal.connect(self.test_start_thread)
        self.input_test_stop_signal.connect(self.test_stop)
        self.input_serial_scan_signal.connect(self.serial_device_scan)
        self.input_serial_connect_signal.connect(self.serial_connect)
        self.input_serial_disconnect_signal.connect(self.serial_disconnect)
        self.input_dc_control_signal.connect(self.dc_control)
        self.input_eload_control_signal.connect(self.eload_control)
        self.input_device_data_scan_signal.connect(self.device_data_scan_flag_change)
        self.input_device_data_scan_time_signal.connect(self.device_data_scan_time_update)
        self.input_monitor_register_num_signal.connect(self.monitor_register_update)
        self.input_device_data_refresh_signal.connect(self.device_data_refresh)

        self.setStyleSheet("font-size: 9pt; font-family: 'Microsoft YaHei UI';")

        self.init_setting()

    def serial_device_scan(self, device):
        """
        扫描电脑上的串口设备
        """
        return_device_list = ''
        serial_device_list = serial.tools.list_ports.comports()
        for i in serial_device_list:
            return_device_list += i[0] + ' #' + i[1] + ','
        self.output_serial_list_signal.emit(device, return_device_list[:-1])

    def device_data_scan_flag_change(self, flag):
        self.device_data_scan_flag = flag

    def serial_connect(self, dc_serial_config, eload_serial_config):
        dc_config = dc_serial_config.split(',')
        eload_config = eload_serial_config.split(',')
        error_flag = False
        if dc_config[-1] != 'False':
            if dc_config[0] != '' and dc_config[1] != '':
                self.dc_device.serial_disconnect()
                try:
                    self.dc_device.device_connect(dc_config[0], dc_config[1], stopbits=2)
                    self.dc_data_scan_thread = threading.Thread(target=self.dc_data_scan, daemon=True)
                    self.dc_data_scan_thread.start()
                except:
                    error_flag = True
                    QMessageBox.warning(self, 'DC连接失败', '请检查串口是否被占用')
            else:
                error_flag = True
                QMessageBox.warning(self, 'DC设置失败', '请检查DC参数是否填写完全')
        if eload_config[-1] != 'False':
            if eload_config[0] != '' and eload_config[1] != '':
                self.eload_device.serial_disconnect()
                try:
                    self.eload_device.device_connect(eload_config[0], eload_config[1], stopbits=2)
                    self.eload_data_scan_thread = threading.Thread(target=self.eload_data_scan, daemon=True)
                    self.eload_data_scan_thread.start()
                except:
                    error_flag = True
                    QMessageBox.warning(self, 'Eload连接失败', '请检查串口是否被占用')
            else:
                error_flag = True
                QMessageBox.warning(self, 'Eload设置失败', '请检查ELoad参数是否填写完全')
        if not error_flag:
            QMessageBox.information(self, 'Success', '设置成功')

    def serial_disconnect(self):
        self.dc_device.serial_disconnect()
        self.eload_device.serial_disconnect()
        QMessageBox.information(self, 'Success', '串口已断开连接')

    def device_data_scan_time_update(self, scan_time):
        if scan_time and scan_time.isdigit():
            self.device_data_scan_time = int(scan_time)

    def dc_data_scan(self):
        while True:
            if self.device_data_scan_flag or self.dc_data_refresh_flag:
                if self.dc_device.connect_flag:
                    dc_output_state = self.dc_device.get_output_state()
                    dc_mode = self.dc_device.get_setting_mode()
                    dc_measure_voltage = self.dc_device.get_measure_voltage()
                    dc_measure_current = self.dc_device.get_measure_current()
                    dc_measure_power = self.dc_device.get_measure_power()
                    upload_data = "{0},{1},{2},{3},{4}".format(dc_output_state, dc_mode, dc_measure_voltage,
                                                               dc_measure_current, dc_measure_power)
                    self.output_device_data_signal.emit("dc", upload_data)
                self.dc_data_refresh_flag = False
            time.sleep(self.device_data_scan_time)

    def eload_data_scan(self):
        while True:
            if self.device_data_scan_flag or self.eload_data_refresh_flag:
                if self.eload_device.connect_flag:
                    eload_input_state = self.eload_device.get_input_state()
                    eload_mode = self.eload_device.get_setting_mode()
                    eload_measure_voltage = self.eload_device.get_measure_voltage()
                    eload_measure_current = self.eload_device.get_measure_current()
                    eload_measure_power = self.eload_device.get_measure_power()
                    upload_data = "{0},{1},{2},{3},{4}".format(eload_input_state, eload_mode, eload_measure_voltage
                                                               , eload_measure_current, eload_measure_power)
                    self.output_device_data_signal.emit("eload", upload_data)
                self.eload_data_refresh_flag = False
            time.sleep(self.device_data_scan_time)

    def device_data_refresh(self):
        self.dc_data_refresh_flag = True
        self.eload_data_refresh_flag = True

    def rule_process(self, log_path, log_first_value, cycle_rule, group_loop_count, dc_init_config):
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
            if i[3] not in re.split(';|,|\t|\n', line) and i[3] != 'Software Time':
                QMessageBox.warning(self, 'Warning', 'Log文件中未找到\'%s\'，请检查输入是否正确' % i[3])
                return

        for i in re.split(';| |,|\t|\n', group_loop_count):
            if i.isdigit() or i == '':
                pass
            else:
                QMessageBox.warning(self, 'Warning', 'Group循环次数只能输入分隔符和数字')
                return

        self.output_register_name_signal.emit(line.replace('\n', ''))
        self.monitor_register_list.clear()
        self.log_file_path = log_path
        self.cycle_rule = temp_cycle_rule
        self.register_line = re.split(';|,|\t|\n', line)
        self.group_loop_count = re.split(';| |,|\t|\n', group_loop_count)

        dc_init_setting = dc_init_config.split(',')
        self.dc_init_mode = (lambda: True if dc_init_setting[0] == 'True' else False)()
        self.dc_init_voltage = dc_init_setting[1]
        self.dc_init_current = dc_init_setting[2]

        QMessageBox.information(self, 'Success', '保存成功')

    def test_start_thread(self):
        if not self.log_file_path or not self.register_line:
            QMessageBox.warning(self, 'Warning', '请先切换到"规则设定"页面，按OK键保存设置。')
            return False
        for i in self.cycle_rule:
            if re.search(str(i), 'Charge', re.IGNORECASE) and not self.dc_device.connect_flag:
                QMessageBox.warning(self, 'Warning', '未设置DC串口参数')
                return False
            if re.search(str(i), 'Discharge', re.IGNORECASE) and not self.eload_device.connect_flag:
                QMessageBox.warning(self, 'Warning', '未设置Eload串口参数')
                return False

        self.test_status = True
        self.log_data_update_thread = threading.Thread(target=self.log_data_update, daemon=True)
        self.log_data_update_thread.start()

        self.test_step_thread = threading.Thread(target=self.test_step, daemon=True)
        self.test_step_thread.start()

        self.output_test_status_signal.emit(True)

    def test_stop(self):
        self.test_status = False
        self.output_test_status_signal.emit(False)

    def log_data_update(self):
        log_file = open(self.log_file_path, 'rb')
        line = []
        while self.test_status:
            offset = -200
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
                    offset = -200
                    continue
            if self.test_status:
                self.register_data = re.split(';|,|\t|\n', line[-1].decode('utf-8'))
                self.output_register_value_signal.emit(line[-1].decode('utf-8').replace('\n', ''))

                monitor_register_name = ""
                monitor_register_value = ""
                for i in self.monitor_register_list:
                    monitor_register_name += (self.register_line[i] + ',')
                    monitor_register_value += (self.register_data[i] + ',')
                self.output_monitor_register_signal.emit(monitor_register_name[:-1], monitor_register_value[:-1])
                time.sleep(0.3)

    def monitor_register_update(self, flag, num):
        if flag:
            self.monitor_register_list.append(num)
        else:
            self.monitor_register_list.remove(num)

    def test_step(self):
        step_num = 0
        group_current_num = ''
        group_current_cycle_count = 1

        while self.test_status:
            if self.cycle_rule[step_num][1] == group_current_num:
                if self.cycle_rule[step_num][0] == 'True' and self.test_status:
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

                    # 充放电命令
                    self.test_action_start(self.cycle_rule[step_num][2], self.cycle_rule[step_num][8],
                                           self.cycle_rule[step_num][9], self.device_init_flag)
                    self.device_init_flag = True
                    # 等待停止条件触发
                    limit_time_begin = time.time()
                    limit_timeout_flag = False
                    software_begin_time = time.time()
                    while self.test_status:
                        current_limit_time = time.time() - limit_time_begin
                        if current_limit_time < int(self.cycle_rule[step_num][7]):
                            self.output_test_status_table_signal.emit(5, '%.2f / %s' % (
                                current_limit_time, self.cycle_rule[step_num][7]), False)
                        else:
                            self.output_test_status_table_signal.emit(5, '%.2f / %s (Timeout)' % (
                                current_limit_time, self.cycle_rule[step_num][7]), False)
                            limit_timeout_flag = True
                            break

                        if (len(self.register_line) - 5) < len(self.register_data) <= len(
                                self.register_line):  # 检查新数据行是否有数据缺失
                            if 'Software Time' in self.cycle_rule[step_num][3]:
                                temp_register_value = round(time.time() - software_begin_time, 2)
                            else:
                                temp_register_value = self.register_data[
                                    self.register_line.index(self.cycle_rule[step_num][3])]
                            if judge.judge(temp_register_value, self.cycle_rule[step_num][5],
                                           self.cycle_rule[step_num][4]):
                                self.output_test_status_table_signal.emit(4, '%s %s %s 停止条件触发' % (
                                    temp_register_value, self.cycle_rule[step_num][4], self.cycle_rule[step_num][5]),
                                                                          False)
                                break
                            else:
                                self.output_test_status_table_signal.emit(4, '%s %s %s 未满足停止条件' % (
                                    temp_register_value, self.cycle_rule[step_num][4], self.cycle_rule[step_num][5]),
                                                                          False)
                        else:
                            self.output_test_status_table_signal.emit(4, '%s %s %s 未满足停止条件' % (
                                '', self.cycle_rule[step_num][4], self.cycle_rule[step_num][5]), False)
                        time.sleep(0.1)

                    # 充放电停止
                    if self.cycle_rule[step_num][-1] == 'dontstop' and self.test_status:
                        # 如果有dontstop标志位，下一阶段不对充放电设备进行初始化，且不关闭充放电设备
                        self.device_init_flag = False
                    else:
                        self.test_action_stop()

                    if limit_timeout_flag:
                        break

                    # 等待阶段
                    begin_wait_time = time.time()
                    while self.cycle_rule[step_num][6] != '' and self.test_status:
                        current_wait_time = time.time() - begin_wait_time
                        self.output_test_status_table_signal.emit(6, '%.2f / %s' % (
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
                            break
                        # 如果循环组为完成循环次数，step_num取余继续继续测试
                        elif group_current_cycle_count < int(self.group_loop_count[int(group_current_num) - 1]):
                            group_current_cycle_count += 1
                            step_num = step_num % len(self.cycle_rule)

                    else:  # step计数未溢出
                        # 1. 判断该step是否有Group编号
                        # 2. 判断该Group循环是否完成
                        if self.cycle_rule[step_num][1] != group_current_num:
                            if (group_current_num != '' and
                                    group_current_cycle_count < int(
                                        self.group_loop_count[int(group_current_num) - 1])):
                                group_current_cycle_count += 1
                            else:
                                group_current_num = self.cycle_rule[step_num][1]
                                group_current_cycle_count = 1
            elif group_current_num == '':
                group_current_num = self.cycle_rule[step_num][1]
            else:
                step_num = (step_num + 1) % len(self.cycle_rule)
        self.test_stop()

    def test_action_start(self, action, value1, value2, init=True):
        if init:
            self.test_action_stop()

        if action == 'Charge':
            if self.dc_device.connect_flag:
                self.dc_control('voltage', value1)
                self.dc_control('current', value2)
                self.dc_control('output', 'on')
                return True
            else:
                return False
        elif action == 'Discharge':
            if self.dc_device.connect_flag:
                self.eload_control(value1, value2)
                if value1 == 'TCC':
                    self.eload_control('input', 'on')
                    self.eload_control('input', 'off')
                    self.eload_control('input', 'on')
                else:
                    self.eload_control('input', 'on')
                return True
            else:
                return False
        elif action == 'None':
            return True
        else:
            return False

    def test_action_stop(self):
        self.eload_control('input', 'off')
        if self.dc_init_mode:
            self.dc_control('current', self.dc_init_current)
            self.dc_control('voltage', self.dc_init_voltage)
            self.dc_control('output', 'on')
        else:
            self.dc_control('output', 'off')

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
            return True
        else:
            return False

    def eload_control(self, config, value):
        if self.eload_device.connect_flag:
            if re.search(config, 'CC', re.IGNORECASE):
                self.eload_device.set_cc_mode(value)
            elif re.search(config, 'CP', re.IGNORECASE):
                self.eload_device.set_cp_mode(value)
            elif re.search(config, 'CR', re.IGNORECASE):
                self.eload_device.set_cr_mode(value)
            elif re.search(config, 'TCC', re.IGNORECASE):
                tcc_setting = re.split('@|,|;', value)
                self.eload_device.set_tran_cc_mode(tcc_setting[0], tcc_setting[1], tcc_setting[2], tcc_setting[3])
            elif re.search(config, 'TCP', re.IGNORECASE):
                tcp_setting = re.split('@|,|;', value)
                self.eload_device.set_tran_cp_mode(tcp_setting[0], tcp_setting[1], tcp_setting[2], tcp_setting[3])
            elif config == 'input' and value == 'on':
                self.eload_device.input_on()
            elif config == 'input' and value == 'off':
                self.eload_device.input_off()
            return True
        else:
            return False

    def init_setting(self):
        if os.path.exists('temp.ini'):
            self.serial_control_tab.serial_init('temp.ini')
            self.rule_tab.load_rule('temp.ini')

    def closeEvent(self, event):
        if self.test_status:
            reply = QMessageBox.question(self, u'警告', u'正在测试，确认退出?', QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.device_data_scan_flag = False
                event.accept()
            else:
                event.ignore()
        else:
            self.device_data_scan_flag = False
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('fusion'))
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
