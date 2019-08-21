import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLabel, \
    QLineEdit, QTextEdit, QFileDialog, QMessageBox, QProgressDialog, QApplication
from PyQt5.QtCore import Qt
from Tetris import *


class Yiji(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 750, 550)
        self.setWindowTitle('gr_app')

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

        self.btn4 = QPushButton('Tetris', self)

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
        h1.addWidget(self.btn4)

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
        key_word = self.line2.text()
        file_dir = self.line1.text()
        if self.step != 0 or self.file_num != 0 or self.found != 0:
            QMessageBox.information(self, "查找", "请先点击清空按钮清除缓存", QMessageBox.Yes)
        elif file_dir == '' or not os.path.exists(file_dir):
            QMessageBox.information(self, "查找", "文件夹不存在", QMessageBox.Yes)
        elif key_word == '':
            QMessageBox.information(self, "查找", "请先输入要查找的关键字", QMessageBox.Yes)
        else:
            self.get_file_num(file_dir)

            self.qpd = QProgressDialog(self)
            self.qpd.setWindowTitle('查找')
            self.qpd.setLabelText('正在查找…')
            self.qpd.setWindowModality(Qt.WindowModal)
            self.qpd.setRange(0, self.file_num)

            if not self.cb3.isChecked():
                self.file_search(file_dir, key_word)
            else:
                self.grep(file_dir, key_word)

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

    def grep(self, cur_dir, key_word):
        if self.qpd.wasCanceled():
            return
        if self.cb2.isChecked():
            f = open('grep.txt', 'a')

        try:
            for each in os.listdir(cur_dir):
                if cur_dir[-1] == '/':
                    cur_dir = cur_dir[:-1]

                self.step += 1
                self.qpd.setValue(self.step)
                # print(cur_dir, each, self.step, self.file_num)

                if os.path.isdir(cur_dir + '/' + each) and cur_dir.split('/')[-1][0] != '.':
                    self.grep(cur_dir + '/' + each, key_word)
                else:
                    if self.cb1.isChecked():
                        with open(cur_dir + '/' + each) as fp:
                            count = 0
                            try:
                                for line in fp.readlines():
                                    if key_word.lower() in line.lower():
                                        count += 1
                                        self.found += 1
                                        self.text.append(cur_dir + '/' + each + ' line ' + str(count) + ' ' + line)
                                        if self.cb2.isChecked():
                                            print(cur_dir + '/' + each + ' line ' + str(count) + ' ' + line, file=f)
                            except UnicodeError:
                                pass
                    else:
                        with open(cur_dir + '/' + each) as fp:
                            count = 0
                            try:
                                for line in fp.readlines():
                                    if key_word in line:
                                        count += 1
                                        self.found += 1
                                        self.text.append(cur_dir + '/' + each + ' line ' + str(count) + ' ' + line)
                                        if self.cb2.isChecked():
                                            print(cur_dir + '/' + each + ' line ' + str(count) + ' ' + line, file=f)
                            except UnicodeError:
                                pass

        except OSError:
            pass

    def file_search(self, cur_dir, key_word):
        if self.qpd.wasCanceled():
            return
        if self.cb2.isChecked():
            f = open('file_search.txt', 'a')
        try:
            for each in os.listdir(cur_dir):
                if cur_dir[-1] == '/':
                    cur_dir = cur_dir[:-1]

                self.step += 1
                self.qpd.setValue(self.step)
                # print(self.step, self.file_num)

                if self.cb1.isChecked():
                    if key_word.lower() in each.lower():
                        self.found += 1
                        self.text.append(cur_dir + '/' + each)
                        if self.cb2.isChecked():
                            print(cur_dir + '/' + each, file=f)
                else:
                    if key_word in each:
                        self.found += 1
                        self.text.append(cur_dir + '/' + each)
                        if self.cb2.isChecked():
                            print(cur_dir + '/' + each, file=f)

                if os.path.isdir(cur_dir + '/' + each):
                    self.file_search(cur_dir + '/' + each, key_word)
        except OSError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    yiji = Yiji()
    tetris = Tetris()
    yiji.show()
    yiji.btn4.clicked.connect(tetris.show)
    yiji.btn4.clicked.connect(yiji.hide)
    # tetris.btn.clicked.connect(yiji.show)
    # tetris.btn.clicked.connect(tetris.hide)
    sys.exit(app.exec_())
