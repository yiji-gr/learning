import sys
import os
import time
import chardet
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLabel, \
    QLineEdit, QTextEdit, QFileDialog, QMessageBox, QProgressDialog, QApplication
from PyQt5.QtCore import Qt


class Yiji(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 750, 550)
        self.setWindowTitle('文件查找')

        w1 = QVBoxLayout(self)

        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        h4 = QHBoxLayout()

        btn1 = QPushButton('选择目录', self)
        btn1.clicked.connect(self.on_click1)
        btn1.setShortcut('Ctrl+D')

        btn2 = QPushButton('查找', self)
        btn2.clicked.connect(self.on_click2)
        btn2.setShortcut(Qt.Key_Enter)

        btn3 = QPushButton('清空', self)
        btn3.clicked.connect(self.on_click3)

        self.cb3 = QCheckBox('grep', self)

        self.qlabel1 = QLabel(self)
        self.qlabel1.setText("您选择的目录是：")

        self.line1 = QLineEdit(self)
        # self.line1.setFocusPolicy(False)

        self.cb1 = QCheckBox('忽略大小写', self)

        self.qlabel2 = QLabel(self)
        self.qlabel2.setText("请输入您要搜索的文件或目录的关键字：")

        self.line2 = QLineEdit(self)

        self.cb2 = QCheckBox('输出到文本', self)

        self.text = QTextEdit(self)
        self.text.setLineWrapMode(QTextEdit.NoWrap)

        h1.addWidget(self.cb3)
        h1.addWidget(btn1)
        h1.addWidget(btn2)
        h1.addWidget(btn3)

        h2.addWidget(self.qlabel1)
        h2.addWidget(self.line1)
        h2.addWidget(self.cb1)

        h3.addWidget(self.qlabel2)
        h3.addWidget(self.line2)
        h3.addWidget(self.cb2)

        h4.addWidget(self.text)

        w1.addLayout(h1)
        w1.addLayout(h2)
        w1.addLayout(h3)
        w1.addLayout(h4)

        self.step = 0
        self.file_num = 0
        self.found = 0

    def get_file_num(self, cur_dir):
        try:
            for each in os.listdir(cur_dir):
                if cur_dir[-1] == '/':
                    cur_dir = cur_dir[:-1]
                self.file_num += 1
                if os.path.isdir(cur_dir + '/' + each):
                    self.get_file_num(cur_dir + '/' + each)
        except OSError:
            pass

    def on_click1(self):
        file_dir = QFileDialog.getExistingDirectory(self)
        self.line1.setText(file_dir)

    def on_click2(self):
        file_dir = self.line1.text()
        self.key_word = self.line2.text()
        if self.step != 0 or self.file_num != 0 or self.found != 0:
            QMessageBox.information(self, "查找", "请先点击清空按钮清除缓存", QMessageBox.Yes)
        elif file_dir == '' or not os.path.exists(file_dir):
            QMessageBox.information(self, "查找", "文件夹不存在", QMessageBox.Yes)
        elif self.key_word == '':
            QMessageBox.information(self, "查找", "请先输入要查找的关键字", QMessageBox.Yes)
        else:
            self.get_file_num(file_dir)

            self.qpd = QProgressDialog(self)
            self.qpd.setWindowTitle('查找')
            self.qpd.setLabelText('正在查找…')
            self.qpd.setWindowModality(Qt.WindowModal)
            self.qpd.setRange(0, self.file_num)

            if not self.cb3.isChecked():
                self.file_search(file_dir)
            else:
                self.grep(file_dir)

            self.qpd.setValue(self.file_num)

            if not self.cb3.isChecked():
                QMessageBox.information(self, "查找结果", "总计" + str(self.found) + "个")
            else:
                QMessageBox.information(self, "查找结果", "总计" + str(self.found) + "行")

    def on_click3(self):
        self.step = 0
        self.file_num = 0
        self.found = 0
        self.text.setText('')
        if os.path.exists('file_search.txt'):
            os.remove('file_search.txt')
        if os.path.exists('grep.txt'):
            os.remove('grep.txt')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter:
            self.on_click2()
        elif e.key() == Qt.Key_Escape:
            self.close()

    def read_file(self, file_path):     # 全面但是速度比较慢
        f = open(file_path, mode="rb")
        data = f.read()
        f.close()
        res = chardet.detect(data)
        try:
            with open(file_path, encoding=res['encoding']) as file:
                return file.readlines()
        except UnicodeError:
            # print('UnicodeError', file_path)
            pass

    def read_file2(self, file_path):
        encoding_list = ['utf-8', 'gbk', 'ansi', 'gb2312', 'gb18030', 'big5', 'cp936', 'utf-16', 'utf-32']
        for encoding in encoding_list:
            try:
                with open(file_path, encoding=encoding) as f:
                    return f.readlines()
            except UnicodeError:
                pass

    def grep(self, cur_dir):
        if self.cb2.isChecked():
            f = open('grep.txt', 'a')

        try:
            for each in os.listdir(cur_dir):
                if self.qpd.wasCanceled():
                    return
                if cur_dir[-1] == '/':
                    cur_dir = cur_dir[:-1]

                self.step += 1
                self.qpd.setValue(self.step)
                file_path = cur_dir + '/' + each
                # print(cur_dir, each, self.step, self.file_num)

                if os.path.isdir(file_path):
                    self.grep(file_path)
                else:
                    lines = self.read_file2(file_path)
                    if lines is None:
                        continue
                    line_count = 0
                    for line in lines:
                        line_count += 1
                        if self.key_word in line or (self.cb1.isChecked() and self.key_word.lower() in line.lower()):
                            self.found += 1
                            show_message = file_path + '    line ' + str(line_count) + '    ' + line.strip()
                            self.text.append(show_message)
                            if self.cb2.isChecked():
                                print(show_message, file=f)

        except OSError:
            # print(cur_dir, 'OSError')
            pass

    def file_search(self, cur_dir):
        if self.cb2.isChecked():
            f = open('file_search.txt', 'a')
        try:
            for each in os.listdir(cur_dir):
                if self.qpd.wasCanceled():
                    return
                if cur_dir[-1] == '/':
                    cur_dir = cur_dir[:-1]

                self.step += 1
                self.qpd.setValue(self.step)
                # print(self.step, self.file_num)

                if self.key_word in each or (self.cb1.isChecked() and self.key_word.lower() in each.lower()):
                    self.found += 1
                    show_message = cur_dir + '/' + each
                    self.text.append(show_message)
                    if self.cb2.isChecked():
                        print(show_message, file=f)

                if os.path.isdir(cur_dir + '/' + each):
                    self.file_search(cur_dir + '/' + each)
        except OSError:
            # print(cur_dir, 'OSError')
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    yiji = Yiji()
    yiji.show()
    sys.exit(app.exec_())
