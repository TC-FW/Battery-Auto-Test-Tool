import re

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from homepage import ui_serial_control_tab


class SerialControlTab(QMainWindow, ui_serial_control_tab.Ui_Form):
    output_serial_scan_signal = QtCore.pyqtSignal(str)
    output_serial_connect_signal = QtCore.pyqtSignal(str, str)
    output_dc_control_signal = QtCore.pyqtSignal(str, str)
    output_eload_control_signal = QtCore.pyqtSignal(str, str)

    input_serial_list_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent, tab):
        super(SerialControlTab, self).__init__(parent)
        self.setupUi(tab)

        self.dc_baud_combobox.setCurrentText('57600')
        self.eload_baud_combobox.setCurrentText('57600')

        self.dc_serial_combobox.clicked.connect(lambda: self.output_serial_scan_signal.emit('dc'))
        self.eload_serial_combobox.clicked.connect(lambda: self.output_serial_scan_signal.emit('eload'))
        self.serial_config_enter_button.clicked.connect(self.serial_connect)

        self.dc_voltage_set_button.clicked.connect(
            lambda: self.output_dc_control_signal.emit('voltage', self.dc_voltage_input.text()))
        self.dc_current_set_button.clicked.connect(
            lambda: self.output_dc_control_signal.emit('current', self.dc_current_input.text()))
        self.dc_output_on_button.clicked.connect(
            lambda: self.output_dc_control_signal.emit('output', 'on'))
        self.dc_output_off_button.clicked.connect(
            lambda: self.output_dc_control_signal.emit('output', 'off'))

        self.eload_mode_set_button.clicked.connect(
            lambda: self.output_eload_control_signal.emit(self.eload_mode_combobox.currentText(),
                                                          self.eload_mode_value_input.text()))
        self.eload_input_on_button.clicked.connect(
            lambda: self.output_eload_control_signal.emit('input', 'on'))
        self.eload_input_off_button.clicked.connect(
            lambda: self.output_eload_control_signal.emit('input', 'off'))

        self.input_serial_list_signal.connect(self.serial_device_update)

    def serial_device_update(self, device, serial_list):
        """
        ??????????????????????????????
        """
        serial_device_list = serial_list.split(',')
        if device == 'dc':
            self.dc_serial_combobox.clear()  # ????????????????????????
            for i in serial_device_list:
                self.dc_serial_combobox.addItem(str(i))  # ?????????????????????

        elif device == 'eload':
            self.eload_serial_combobox.clear()  # ????????????????????????
            for i in serial_device_list:
                self.eload_serial_combobox.addItem(str(i))  # ?????????????????????

    def serial_connect(self):
        if self.dc_serial_combobox.currentText():
            dc_connect_com = re.match(r'(.*?) #', str(self.dc_serial_combobox.currentText())).group(1)
        else:
            dc_connect_com = ''
        connect_bps = self.dc_baud_combobox.currentText()
        dc_serial_config = str(dc_connect_com) + ',' + str(connect_bps)

        if self.eload_serial_combobox.currentText():
            eload_connect_com = re.match(r'(.*?) #', str(self.eload_serial_combobox.currentText())).group(1)
        else:
            eload_connect_com = ''
        connect_bps = self.eload_baud_combobox.currentText()
        eload_serial_config = str(eload_connect_com) + ',' + str(connect_bps)

        self.output_serial_connect_signal.emit(dc_serial_config, eload_serial_config)
