import re
import time
import serial


class HengHuiDC:
    def __init__(self):
        self.ser = serial.Serial()
        self.connect_flag = False
        self.control_flag = False

    def device_connect(self, port, baud, stopbits):
        self.ser = serial.Serial(port=port, baudrate=baud, stopbits=stopbits)
        self.connect_flag = True

    def device_write_data(self, data):
        self.ser.flushOutput()
        self.ser.write(data.encode('utf-8'))

    def serial_read_message(self):
        temp = ''
        time_start = time.time()
        while True:
            if self.ser.in_waiting:
                string = self.ser.read_all().decode('utf-8', 'ignore')
                temp += string
            if (time.time() - time_start) > 0.05:
                break
        return temp

    def set_current(self, current):
        error_count = 0
        while self.control_flag:
            continue
        while True:
            self.control_flag = True
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

    def set_voltage(self, voltage):
        error_count = 0
        while self.control_flag:
            continue
        while True:
            self.control_flag = True
            self.ser.write(('VOLT ' + voltage + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('VOLT?\n'.encode('utf-8'))
            read_back_voltage = self.serial_read_message().replace('\n', '')
            if self.check_float(read_back_voltage) and float(read_back_voltage) == float(voltage):
                self.control_flag = False
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                self.control_flag = False
                return False

    def output_on(self):
        error_count = 0
        while self.control_flag:
            continue
        while True:
            self.control_flag = True
            self.ser.write('OUTPUT ON\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('OUTPUT?\n'.encode('utf-8'))
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

    def output_off(self):
        error_count = 0
        while self.control_flag:
            continue
        while True:
            self.control_flag = True
            self.ser.write('OUTPUT OFF\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('OUTPUT?\n'.encode('utf-8'))
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

    def get_output_state(self):
        error_count = 0
        while self.control_flag:
            continue
        while True:
            self.control_flag = True
            self.ser.write('OUTPUT?\n'.encode('utf-8'))
            state = self.serial_read_message().replace('\n', '')
            state = state if state else 'None'
            self.control_flag = False
            return state

    def get_setting_mode(self):
        while self.control_flag:
            continue
        self.control_flag = True
        self.ser.write(':STAT:OPER:COND?\n'.encode('utf-8'))
        status = self.serial_read_message().replace('\n', '')
        if status != '' and not re.search("[^\+,0-9]", status):
            if int(status) == 512:
                mode = "CV"
            elif int(status) == 1024:
                mode = "CC"
            elif int(status) == 0:
                mode = " "
            else:
                mode = "None"
        else:
            mode = "None"
        self.ser.write('CURR?\n'.encode('utf-8'))
        setting_current = self.serial_read_message().replace('\n', '')
        setting_current = float(setting_current) if self.check_float(setting_current) else 'None'
        self.ser.write('VOLT?\n'.encode('utf-8'))
        setting_voltage = self.serial_read_message().replace('\n', '')
        setting_voltage = float(setting_voltage) if self.check_float(setting_voltage) else 'None'
        self.control_flag = False
        return "{0},{1}V\n{2}A".format(mode, setting_voltage, setting_current)

    def get_measure_current(self):
        while self.control_flag:
            continue
        self.control_flag = True
        self.ser.write(':MEAS:CURR?\n'.encode('utf-8'))
        current = self.serial_read_message().replace('\n', '')
        current = float(current) if self.check_float(current) else 'None'
        self.control_flag = False
        return current

    def get_measure_voltage(self):
        while self.control_flag:
            continue
        self.control_flag = True
        self.ser.write(':MEAS:VOLT?\n'.encode('utf-8'))
        voltage = self.serial_read_message().replace('\n', '')
        voltage = float(voltage) if self.check_float(voltage) else 'None'
        self.control_flag = False
        return voltage

    def get_measure_power(self):
        while self.control_flag:
            continue
        self.control_flag = True
        self.ser.write(':MEAS:POW?\n'.encode('utf-8'))
        power = self.serial_read_message().replace('\n', '')
        power = float(power) if self.check_float(power) else 'None'
        self.control_flag = False
        return power

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
