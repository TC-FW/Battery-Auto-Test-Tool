import re
import threading
import time

import serial


class HengHuiEload:
    def __init__(self):
        self.ser = serial.Serial()
        self.tran_cp_flag = False
        self.connect_flag = False
        self.control_flag = False

    def device_connect(self, port, baud, stopbits):
        self.ser = serial.Serial(port=port, baudrate=baud, stopbits=stopbits)
        self.connect_flag = True

    def serial_read_message(self):
        temp = ''
        time_start = time.time()
        while True:
            if self.ser.in_waiting:
                string = self.ser.read_all().decode('utf-8')
                temp += string
            if (time.time() - time_start) > 0.05:
                break
        return temp

    def set_cc_mode(self, current):
        error_count = 0
        while self.control_flag:
            continue
        while True:
            self.control_flag = True
            self.ser.write('MODE CCH\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write(('CURR ' + current + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('CURR?\n'.encode('utf-8'))
            read_back_current = self.serial_read_message().replace('\n', '')
            if self.check_float(read_back_current) and float(read_back_current) == float(current):
                self.control_flag = False
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                self.control_flag = False
                return False

    def set_cp_mode(self, power):
        error_count = 0
        while self.control_flag:
            continue

        while True:
            self.control_flag = True
            self.ser.write('MODE CPV\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write(('POW ' + power + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('POW?\n'.encode('utf-8'))
            read_back_power = self.serial_read_message().replace('\n', '')
            if self.check_float(read_back_power) and float(read_back_power) == float(power):
                self.control_flag = False
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                self.control_flag = False
                return False

    def set_cr_mode(self, resistance):
        error_count = 0
        while self.control_flag:
            continue

        while True:
            self.control_flag = True
            self.ser.write('MODE CRH\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write(('RES ' + resistance + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('RES?\n'.encode('utf-8'))
            read_back_resistance = self.serial_read_message().replace('\n', '')
            if self.check_float(read_back_resistance) and float(read_back_resistance) == float(resistance):
                self.control_flag = False
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                self.control_flag = False
                return False

    def set_tran_cc_mode(self, power_l, time_l, power_h, time_h):
        while self.control_flag:
            continue
        self.control_flag = True
        error_count = 0
        self.ser.write('TRAN ON\n'.encode('utf-8'))
        time.sleep(0.1)
        self.ser.write(':TRAN:MODE CONT\n'.encode('utf-8'))
        time.sleep(0.1)
        self.ser.write(':TRAN:FTIM MIN\n'.encode('utf-8'))
        time.sleep(0.1)
        self.ser.write(':TRAN:RTIM MIN\n'.encode('utf-8'))
        time.sleep(0.1)
        while True:
            self.ser.write((':CURR:LLEV ' + power_l + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write((':TRAN:LTIM ' + time_l + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write((':CURR:HLEV ' + power_h + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write((':TRAN:HTIM ' + time_h + '\n').encode('utf-8'))
            time.sleep(0.1)

            self.ser.write(':CURR:LLEV?\n'.encode('utf-8'))
            read_back_power_l = self.serial_read_message().replace('\n', '')
            self.ser.write(':TRAN:LTIM?\n'.encode('utf-8'))
            read_back_time_l = self.serial_read_message().replace('\n', '')
            self.ser.write(':CURR:HLEV?\n'.encode('utf-8'))
            read_back_power_h = self.serial_read_message().replace('\n', '')
            self.ser.write(':TRAN:HTIM?\n'.encode('utf-8'))
            read_back_time_h = self.serial_read_message().replace('\n', '')

            if ((self.check_float(read_back_power_l) and self.check_float(read_back_time_l) and
                 self.check_float(read_back_power_h) and self.check_float(read_back_time_h)) and
                    (float(read_back_power_l) == float(power_l) and float(read_back_time_l) == float(time_l) and
                     float(read_back_power_h) == float(power_h) and float(read_back_time_h) == float(time_h))):
                self.control_flag = False
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                self.control_flag = False
                return False

    def set_tran_cp_mode(self, power_l, time_l, power_h, time_h):
        tran_cp_thread = threading.Thread(target=self.tran_cp, args=(power_l, time_l, power_h, time_h,), daemon=True)
        tran_cp_thread.start()

    def tran_cp(self, power_l, time_l, power_h, time_h):
        self.tran_cp_flag = True
        while self.tran_cp_flag:
            self.set_cp_mode(power_l)
            time.sleep(int(time_l) - 0.5)
            self.set_cp_mode(power_h)
            time.sleep(int(time_h) - 0.5)

    def input_on(self):
        error_count = 0
        while self.control_flag:
            continue
        while True:
            self.control_flag = True
            self.ser.write('INPUT ON\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('INPUT?\n'.encode('utf-8'))
            read_back_input_status = self.serial_read_message().replace('\n', '')
            if read_back_input_status != '' and read_back_input_status == 'ON':
                self.control_flag = False
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                self.control_flag = False
                return False

    def input_off(self):
        error_count = 0
        while self.control_flag:
            continue
        while True:
            self.control_flag = True
            if self.tran_cp_flag:
                self.tran_cp_flag = False
            self.ser.write('INPUT OFF\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('INPUT?\n'.encode('utf-8'))
            read_back_input_status = self.serial_read_message().replace('\n', '')
            if read_back_input_status != '' and read_back_input_status == 'OFF':
                self.control_flag = False
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                self.control_flag = False
                return False

    def get_input_state(self):
        error_count = 0
        while self.control_flag:
            continue
        while True:
            self.control_flag = True
            self.ser.write('INPUT?\n'.encode('utf-8'))
            value = self.serial_read_message().replace('\n', '')
            value = value if value else 'None'
            self.control_flag = False
            return value

    def get_setting_mode(self):
        while self.control_flag:
            continue
        self.control_flag = True
        self.ser.write('Mode?\n'.encode('utf-8'))
        mode = self.serial_read_message().replace('\n', '')
        self.ser.write('Tran?\n'.encode('utf-8'))
        tran_mode = self.serial_read_message().replace('\n', '')

        if re.search('on', tran_mode, re.I):
            self.ser.write(':CURR:LLEV?\n'.encode('utf-8'))
            read_back_power_l = self.serial_read_message().replace('\n', '')
            self.ser.write(':TRAN:LTIM?\n'.encode('utf-8'))
            read_back_time_l = self.serial_read_message().replace('\n', '')
            self.ser.write(':CURR:HLEV?\n'.encode('utf-8'))
            read_back_power_h = self.serial_read_message().replace('\n', '')
            self.ser.write(':TRAN:HTIM?\n'.encode('utf-8'))
            read_back_time_h = self.serial_read_message().replace('\n', '')
            self.control_flag = False
            return "{0},{1},{2},{3},{4}".format('TRAN', read_back_power_l, read_back_time_l, read_back_power_h, read_back_time_h)
        else:
            if re.search('cc', mode, re.I):
                self.ser.write('curr?\n'.encode('utf-8'))
                value = self.serial_read_message().replace('\n', '')
                value = (value + 'A') if value else 'None'
            elif re.search('cp', mode, re.I):
                self.ser.write('POW?\n'.encode('utf-8'))
                value = self.serial_read_message().replace('\n', '')
                value = (value + 'W') if value else 'None'
            elif re.search('cr', mode, re.I):
                self.ser.write('RES?\n'.encode('utf-8'))
                value = self.serial_read_message().replace('\n', '')
                value = (value + 'Ω') if value else 'None'
            else:
                return "None,None"
            self.control_flag = False
            return "{0},{1}".format(mode, value)

    def get_measure_current(self):
        while self.control_flag:
            continue
        self.control_flag = True
        self.ser.write(':MEAS:CURR?\n'.encode('utf-8'))
        current = self.serial_read_message().replace('\n', '')
        current = (current + 'A') if current else 'None'
        self.control_flag = False
        return current

    def get_measure_voltage(self):
        while self.control_flag:
            continue
        self.control_flag = True
        self.ser.write(':MEAS:VOLT?\n'.encode('utf-8'))
        voltage = self.serial_read_message().replace('\n', '')
        voltage = (voltage + 'V') if voltage else 'None'
        self.control_flag = False
        return voltage

    @staticmethod
    def check_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def serial_disconnect(self):
        self.ser.close()
        self.connect_flag = False
