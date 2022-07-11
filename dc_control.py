import time
import serial


class HengHuiDC:
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

    def set_current(self, current):
        error_count = 0
        while True:
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

    def set_voltage(self, voltage):
        error_count = 0
        while True:
            self.ser.write(('VOLT ' + voltage + '\n').encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('VOLT?\n'.encode('utf-8'))
            read_back_voltage = self.serial_read_message().replace('\n', '')
            if self.check_float(read_back_voltage) and float(read_back_voltage) == float(voltage):
                return True
            elif error_count <= 5:
                continue
            else:
                return False

    def output_on(self):
        error_count = 0
        while True:
            self.ser.write('OUTPUT ON\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('OUTPUT?\n'.encode('utf-8'))
            read_back_input_status = self.serial_read_message().replace('\n', '')
            if read_back_input_status != '' and read_back_input_status == 'ON':
                return True
            elif error_count <= 5:
                error_count += 1
                continue
            else:
                return False

    def output_off(self):
        error_count = 0
        while True:
            self.ser.write('OUTPUT OFF\n'.encode('utf-8'))
            time.sleep(0.1)
            self.ser.write('OUTPUT?\n'.encode('utf-8'))
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
