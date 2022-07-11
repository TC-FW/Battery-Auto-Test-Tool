import time

import serial


class HengHuiEload:
    def __init__(self):
        self.ser = serial.Serial()
        self.connect_flag = False

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
            if (time.time() - time_start) > 0.5:
                break
        return temp

    def write_info(self, string):
        self.ser.write((string + '\n').encode('utf-8'))

    def set_cc_mode(self, current):
        error_count = 0
        while True:
            self.ser.write('MODE CCH\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write(('CURR ' + current + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('CURR?\n'.encode('utf-8'))
            read_back_current = self.serial_read_message().replace('\n', '')
            if self.check_float(read_back_current) and float(read_back_current) == float(current):
                return True
            elif error_count <= 5:
                continue
            else:
                return False

    def set_cp_mode(self, power):
        error_count = 0
        while True:
            self.ser.write('MODE CPC\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write(('POW ' + power + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('POW?\n'.encode('utf-8'))
            read_back_power = self.serial_read_message().replace('\n', '')
            if self.check_float(read_back_power) and float(read_back_power) == float(power):
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                return False

    def set_cr_mode(self, resistance):
        error_count = 0
        while True:
            self.ser.write('MODE CRH\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write(('RES ' + resistance + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('RES?\n'.encode('utf-8'))
            read_back_resistance = self.serial_read_message().replace('\n', '')
            if self.check_float(read_back_resistance) and float(read_back_resistance) == float(resistance):
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                return False

    def set_tran_cc_mode(self, current_l, time_l, current_h, time_h):
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
            self.ser.write((':CURR:LLEV ' + current_l + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write((':TRAN:LTIM ' + time_l + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write((':CURR:HLEV ' + current_h + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write((':TRAN:HTIM ' + time_h + '\n').encode('utf-8'))
            time.sleep(0.1)

            self.ser.write(':CURR:LLEV?\n'.encode('utf-8'))
            read_back_current_l = self.serial_read_message().replace('\n', '')
            self.ser.write(':TRAN:LTIM?\n'.encode('utf-8'))
            read_back_time_l = self.serial_read_message().replace('\n', '')
            self.ser.write(':CURR:HLEV?\n'.encode('utf-8'))
            read_back_current_h = self.serial_read_message().replace('\n', '')
            self.ser.write(':TRAN:HTIM?\n'.encode('utf-8'))
            read_back_time_h = self.serial_read_message().replace('\n', '')

            if ((self.check_float(read_back_current_l) and self.check_float(read_back_time_l) and
                 self.check_float(read_back_current_h) and self.check_float(read_back_time_h)) and
                    (float(read_back_current_l) == float(current_l) and float(read_back_time_l) == float(time_l) and
                     float(read_back_current_h) == float(current_h) and float(read_back_time_h) == float(time_h))):
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                return False

    def input_on(self):
        error_count = 0
        while True:
            self.ser.write('INPUT ON\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('INPUT?\n'.encode('utf-8'))
            read_back_input_status = self.serial_read_message().replace('\n', '')
            if read_back_input_status != '' and read_back_input_status == 'ON':
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                return False

    def input_off(self):
        error_count = 0
        while True:
            self.ser.write('INPUT OFF\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('INPUT?\n'.encode('utf-8'))
            read_back_input_status = self.serial_read_message().replace('\n', '')
            if read_back_input_status != '' and read_back_input_status == 'OFF':
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                return False

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
