import os
import re

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QComboBox, QCheckBox, QHeaderView, QFileDialog, QTableWidgetItem, QMenu, \
    QAbstractItemView
import configparser
from homepage import ui_rule_tab


class RuleTab(QMainWindow, ui_rule_tab.Ui_Form):
    output_rule_signal = QtCore.pyqtSignal(str, str, str, str, str)

    def __init__(self, parent, tab):
        super(RuleTab, self).__init__(parent)
        self.setupUi(tab)
        # self.rule_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.rule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.enter_button.clicked.connect(self.rule_set)
        self.add_rule_button.clicked.connect(self.add_rule)
        self.del_rule_button.clicked.connect(self.del_rule)
        self.log_select_button.clicked.connect(self.log_file_select)
        self.save_setting_button.clicked.connect(self.save_rule_file_select)
        self.load_setting_button.clicked.connect(self.load_rule_file_select)

        self.rule_table.setDragEnabled(True)
        self.rule_table.setAcceptDrops(True)
        self.rule_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.register_list = ['Software Time']
        self.copy_row_num = None

        self.file_select_input.textChanged.connect(self.register_list_update)
        self.log_first_value_combox.currentTextChanged.connect(self.register_list_update)

        self.rule_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.rule_table.customContextMenuRequested.connect(self.context_menu)

    def context_menu(self, pos):
        row_num = -1
        for i in self.rule_table.selectionModel().selection().indexes():
            row_num = i.row()
        menu = QMenu()  # 实例化菜单
        item1 = menu.addAction(u"插入规则")
        item2 = menu.addAction(u"删除规则")
        item3 = menu.addAction(u"复制规则")
        item4 = menu.addAction(u"插入复制规则")

        if self.copy_row_num is not None:
            item4.setEnabled(True)
        else:
            item4.setEnabled(False)

        action = menu.exec_(self.rule_table.mapToGlobal(pos))

        if action == item1:
            self.add_rule(row_num)
        elif action == item2:
            self.del_rule(row_num)
        elif action == item3:
            self.copy_row_num = row_num
        elif action == item4:
            if row_num >= 0:
                if self.copy_row_num >= row_num:
                    self.copy_row_num += 1
            elif row_num == -1:
                row_num = self.rule_table.rowCount()
            self.add_rule(row_num)
            for i in range(self.rule_table.columnCount()):
                if i == 0:
                    if self.rule_table.cellWidget(self.copy_row_num, i).isChecked:
                        self.rule_table.cellWidget(row_num, i).setChecked(True)
                    else:
                        self.rule_table.cellWidget(row_num, i).setChecked(False)
                elif i == 2 or i == 3 or i == 4:
                    self.rule_table.cellWidget(row_num, i).setCurrentText(self.rule_table.cellWidget(self.copy_row_num, i).currentText())
                elif self.rule_table.item(self.copy_row_num, i) is not None:
                    self.rule_table.setItem(row_num, i, QTableWidgetItem(self.rule_table.item(self.copy_row_num, i).text()))

    def add_rule(self, select_num=-1):
        if select_num is not False and select_num is not None and select_num >= 0:
            row_num = select_num
            self.rule_table.insertRow(row_num)
        else:
            self.rule_table.setRowCount(self.rule_table.rowCount() + 1)
            row_num = self.rule_table.rowCount() - 1

        combox1 = QComboBox()
        combox1.addItems(['Charge', 'Discharge', 'None'])
        combox1.setEditable(True)

        checkbox = QCheckBox()
        checkbox.setChecked(True)

        register_combox = QComboBox()
        register_combox.addItems(self.register_list)
        register_combox.setEditable(True)
        register_combox.view().setTextElideMode(QtCore.Qt.ElideNone)
        register_combox.view().setFixedWidth(150)

        combox2 = QComboBox()
        combox2.addItems(['>', '<', '=', '>=', '<=', 'Set', 'Reset'])
        combox2.setEditable(True)

        self.rule_table.setCellWidget(row_num, 0, checkbox)
        self.rule_table.setCellWidget(row_num, 2, combox1)
        self.rule_table.setCellWidget(row_num, 3, register_combox)
        self.rule_table.setCellWidget(row_num, 4, combox2)
        self.rule_table.setItem(row_num, 6, QTableWidgetItem('1800'))
        self.rule_table.setItem(row_num, 7, QTableWidgetItem('54000'))

    def del_rule(self, select_num=None):
        if select_num is not False and select_num is not None and select_num >= 0:
            row_num = select_num
        else:
            row_num = self.rule_table.rowCount() - 1

        if self.rule_table.rowCount() > 0:
            self.rule_table.removeRow(row_num)

    def rule_set(self):
        temp_rule = ''
        for i in range(self.rule_table.rowCount()):
            for j in range(self.rule_table.columnCount()):
                if j == 0:
                    temp_rule += str(self.rule_table.cellWidget(i, j).isChecked()) + ','
                elif j == 2 or j == 3 or j == 4:
                    temp_rule += str(self.rule_table.cellWidget(i, j).currentText()) + ','
                elif self.rule_table.item(i, j) is not None:
                    temp_rule += self.rule_table.item(i, j).text() + ','
                else:
                    temp_rule += '' + ','
                if j == self.rule_table.columnCount() - 1:
                    temp_rule = temp_rule[:-1] + ';'

        dc_init_mode = (str(self.dc_init_mode1_checkbox.isChecked()) + ',' + self.dc_init_mode1_v_input.text() +
                        ',' + self.dc_init_mode1_i_input.text())

        self.output_rule_signal.emit(self.file_select_input.text(), self.log_first_value_combox.currentText(),
                                     temp_rule, self.group_cycle_count_input.text(), dc_init_mode)

        if not os.path.exists('temp.ini'):
            file = open('temp.ini', 'w', encoding='utf-8')
            file.close()
        self.save_rule('temp.ini')

        return True

    def log_file_select(self):
        """
        导出文件夹选择
        :return: None
        """
        file_path = self.get_init_path('log path')
        file_name = QFileDialog.getOpenFileName(self, "选取文件", file_path, "Log Files(*.log;*.csv);;All Files(*)")
        if file_name[0]:
            self.file_select_input.setText(file_name[0])
            if file_name[0][-4:] == '.log':
                self.log_first_value_combox.setCurrentText('Sample')
            elif file_name[0][-4:] == '.csv':
                self.log_first_value_combox.setCurrentText('Time')
            self.auto_save_path('temp.ini', 'log path', file_name[0][:file_name[0].rfind('/') + 1])

    def register_list_update(self):
        """
        log数据寄存器名称列表更新
        :return: None
        """
        if not os.path.exists(self.file_select_input.text()):
            return

        file = open(self.file_select_input.text(), 'r')
        begin_line = 0
        while True:
            line = file.readline()
            if begin_line <= 100:
                if self.log_first_value_combox.currentText() == re.split(';|,|\t|\n', line)[0]:
                    break
                else:
                    begin_line += 1
            else:
                return False

        self.register_list = re.split(';|,|\t|\n', line.replace('\n', ''))
        self.register_list.append('Software Time')

        # 更新规则内Register Combobox的数据
        for i in range(self.rule_table.rowCount()):
            temp_value = self.rule_table.cellWidget(i, 3).currentText()
            self.rule_table.cellWidget(i, 3).clear()
            self.rule_table.cellWidget(i, 3).addItems(self.register_list)
            self.rule_table.cellWidget(i, 3).setCurrentText(temp_value)

    def save_rule_file_select(self):
        file_path = self.get_init_path('rule path')
        file_name = QFileDialog.getSaveFileName(self, "选取文件", file_path + '/' + '-LearningSetting', "INI Files(*.ini)")
        if file_name[0]:
            if not os.path.exists(file_name[0]):
                file = open(file_name[0], 'w', encoding='utf-8')
                file.close()
            self.save_rule(file_name[0])
            self.auto_save_path('temp.ini', 'rule path', file_name[0][:file_name[0].rfind('/') + 1])

    def load_rule_file_select(self):
        file_path = self.get_init_path('rule path')
        file_name = QFileDialog.getOpenFileName(self, "选取文件", file_path, "INI Files(*.ini)")
        if file_name[0]:
            self.load_rule(file_name[0])
            self.auto_save_path('temp.ini', 'rule path', file_name[0][:file_name[0].rfind('/') + 1])

    def save_rule(self, file_path):
        config = configparser.ConfigParser()
        config.read(file_path, encoding="utf-8")

        if not config.has_section("Rule"):
            config.add_section("Rule")
        else:
            config.remove_section("Rule")
            config.add_section("Rule")

        config.set('Rule', 'Row_Count', str(self.rule_table.rowCount()))

        for i in range(self.rule_table.rowCount()):
            temp_rule = ''
            for j in range(self.rule_table.columnCount()):
                if j == 0:
                    temp_rule += str(self.rule_table.cellWidget(i, j).isChecked()) + ','
                elif j == 2 or j == 3 or j == 4:
                    temp_rule += str(self.rule_table.cellWidget(i, j).currentText()) + ','
                elif self.rule_table.item(i, j) is not None:
                    temp_rule += self.rule_table.item(i, j).text() + ','
                else:
                    temp_rule += '' + ','
                if j == self.rule_table.columnCount() - 1:
                    config.set('Rule', 'Rule_Setting_' + str(i), temp_rule[:-1])

        config.set('Rule', 'Init Mode Enable', str(self.dc_init_mode1_checkbox.isChecked()))
        config.set('Rule', 'Init Mode V', self.dc_init_mode1_v_input.text())
        config.set('Rule', 'Init Mode I', self.dc_init_mode1_i_input.text())
        config.set('Rule', 'Group Cycle Count', self.group_cycle_count_input.text())

        config.write(open(file_path, 'w', encoding='utf-8'))

    def load_rule(self, file_path):
        config = configparser.ConfigParser()
        config.read(file_path, encoding="utf-8")
        self.rule_table.setRowCount(0)
        if config.has_section("Rule"):
            try:
                for i in range(int(config.get('Rule', 'Row_Count'))):
                    self.add_rule()
                    temp_rule = config.get('Rule', 'Rule_Setting_' + str(i)).split(',')
                    for j in range(self.rule_table.columnCount()):
                        if j == 0:
                            if temp_rule[0] == 'True':
                                self.rule_table.cellWidget(self.rule_table.rowCount() - 1, j).setChecked(True)
                            else:
                                self.rule_table.cellWidget(self.rule_table.rowCount() - 1, j).setChecked(False)
                        elif j == 2 or j == 3 or j == 4:
                            self.rule_table.cellWidget(self.rule_table.rowCount() - 1, j).setCurrentText(temp_rule[j])
                        else:
                            self.rule_table.setItem(self.rule_table.rowCount() - 1, j, QTableWidgetItem(temp_rule[j]))

                if config.get('Rule', 'Init Mode Enable') == 'True':
                    self.dc_init_mode1_checkbox.setChecked(True)

                self.dc_init_mode1_v_input.setText(config.get('Rule', 'Init Mode V'))
                self.dc_init_mode1_i_input.setText(config.get('Rule', 'Init Mode I'))
                self.group_cycle_count_input.setText(config.get('Rule', 'Group Cycle Count'))
                return True

            except:
                return False

    @staticmethod
    def auto_save_path(ini_file_path, path_type, path):
        if not os.path.exists(ini_file_path):
            file = open(ini_file_path, 'w', encoding='utf-8')
            file.close()

        config = configparser.ConfigParser()
        config.read(ini_file_path, encoding="utf-8")

        if not config.has_section("Path"):
            config.add_section("Path")
        config.set("Path", path_type, path)
        config.write(open(ini_file_path, 'w', encoding='utf-8'))

    @staticmethod
    def get_init_path(path_type):
        if os.path.exists('temp.ini'):
            config = configparser.ConfigParser()
            config.read('./temp.ini', encoding="utf-8")

            if config.has_section("Path") and path_type in config.options("Path") and config.get("Path", path_type):
                file_path = config.get("Path", path_type)
            else:
                file_path = os.getcwd()
        else:
            file_path = os.getcwd()
        return file_path
