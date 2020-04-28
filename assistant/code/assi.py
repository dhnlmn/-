# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assistant.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
import socket,select
import time
import json
from PyQt5.QtCore import QTimer





class Thread_2(QThread):  # 线程2 clien
    signal = pyqtSignal(str)  #一定要siganl设置静态变量，全局区
    def __init__(self,ip,port):
        super().__init__()
        self.ip=ip
        self.port=port
    def run(self):
        print("clien 开启")
        try:
            self.connect()
            while True:
                print(55)
                self.rev()
        except:
            self.signal.emit("配置不正确")
    def rev(self):   #收信息
        self.data=self.s.recv(1024)
        if len(self.data):
            self.signal.emit(str(self.data))
    def connect(self):
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.s.connect((self.ip, int(self.port)))

class Thread_1(QThread):  # 线程1 server
    signal = pyqtSignal(str)  #一定要siganl设置静态变量，全局区
    def __init__(self,ip,port):
        super().__init__()
        self.ip=ip
        self.port=port
        self.cli_list = []     #连接的客户端的socket对象列表
    def run(self):
        print("server 开启")
        self.send_messge_s()
    def connect(self):
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)

        self.s.bind((self.ip, int(self.port)))
        self.s.listen(10)
        #self.cli, self.addr = self.s.accept()
    def send_messge_s(self):
        try:
            self.connect()  #服务器上线
            while True:
                select_list = [self.s]   #存储套接字
                select_list.extend(self.cli_list)
                rlist, wlist, xlist = select.select(select_list,[],[]) #监听可读套接字
                print("可读信息"+str(rlist))
                #rlist 中保存了读就绪的客户端的socket对象和server
                for self.sock in rlist:
                    #如果sock是server说明：有新的客户端发起连接请求
                    if self.sock == self.s:
                        #接收客户端的请求
                        print("进入等待")
                        self.cli, self.addr = self.s.accept()
                        print("new connection: ", self.addr)
                        #将该cli追加到 cli_list中
                        self.cli_list.append(self.cli)
                    else:
                        print(2)
                        #如果sock是客户端说明：该客户端有数据可以读
                        self.data = self.sock.recv(1024)
                        self.data=self.data.decode()
                        self.cli=self.sock
                        try:
                            self.data = json.loads(self.data) #异常处理机制区分json和其他类型信息
                        except:
                            pass
                        self.data=str(self.data)    #这里是防止data是int类型触发len()异常
                        if len(self.data):
                            #self.cli.send(b'ok')
                            self.signal.emit(str(self.data))  #发送信息给主线程回调函数，同时线程结束(该线程是否继续进行取决于主线程)
        except:
            self.signal.emit("配置不正确")


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.flag=0 #是否连接的判断
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(836, 780)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.window = QtWidgets.QTextEdit(self.centralwidget)
        self.window.setGeometry(QtCore.QRect(310, 40, 511, 551))
        self.window.setObjectName("window")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 60, 87, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 10, 161, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 56, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 56, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 56, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.label_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_2.setToolTip("")
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 90, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setScaledContents(False)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 170, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setScaledContents(False)
        self.label_4.setObjectName("label_4")
        self.show_ip = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.show_ip.setGeometry(QtCore.QRect(50, 130, 201, 31))
        self.show_ip.setObjectName("show_ip")
        self.show_port = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.show_port.setGeometry(QtCore.QRect(50, 210, 201, 31))
        self.show_port.setObjectName("show_port")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(307, 610, 421, 71))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.send_ms = QtWidgets.QPlainTextEdit(self.widget)
        self.send_ms.setObjectName("send_ms")
        self.horizontalLayout.addWidget(self.send_ms)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(50, 320, 221, 30))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton = QtWidgets.QRadioButton(self.widget1)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_2.addWidget(self.radioButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 836, 26))
        self.menubar.setObjectName("menubar")
        self.ip_B = QtWidgets.QPushButton(self.centralwidget)
        self.ip_B.setGeometry(QtCore.QRect(160, 50, 131, 41))
        self.ip_B.setObjectName("ip_B")
        self.loop_bu = QtWidgets.QCheckBox(self.centralwidget)
        self.loop_bu.setGeometry(QtCore.QRect(50, 400, 91, 19))
        self.loop_bu.setObjectName("loop_bu")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 440, 101, 16))
        self.label_5.setObjectName("label_5")
        self.time_bu = QtWidgets.QTextEdit(self.centralwidget)
        self.time_bu.setGeometry(QtCore.QRect(130, 440, 101, 21))
        self.time_bu.setObjectName("time_bu")
        self.time_bu.setText("1000")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)  #不同信号对应的槽
        self.pushButton.clicked.connect(self.send)
        self.ip_B.clicked.connect(self.write_ip)
        self.radioButton.clicked.connect(self.setcheck)
        self.comboBox.currentIndexChanged['int'].connect(self.get_mode)
        self.pushButton_2.clicked.connect(self.clear)
        self.loop_bu.clicked.connect(self.loop_send)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.window, self.comboBox)
        MainWindow.setTabOrder(self.comboBox, self.pushButton)
        MainWindow.setTabOrder(self.pushButton, self.radioButton)
        MainWindow.setTabOrder(self.radioButton, self.send_ms)
        MainWindow.setTabOrder(self.send_ms, self.show_ip)
        MainWindow.setTabOrder(self.show_ip, self.show_port)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "clien"))
        self.comboBox.setItemText(1, _translate("MainWindow", "server"))
        self.label.setText(_translate("MainWindow", "协议类型"))
        self.label_2.setText(_translate("MainWindow", "网络调试助手"))
        self.label_3.setText(_translate("MainWindow", "输入ip"))
        self.label_4.setText(_translate("MainWindow", "本地端口号"))
        self.pushButton.setText(_translate("MainWindow", "发送"))
        self.radioButton.setText(_translate("MainWindow", "连接"))
        self.pushButton_2.setText(_translate("MainWindow", "清空消息"))
        self.ip_B.setText(_translate("MainWindow", "一键填写本机ip"))
        self.label_5.setText(_translate("MainWindow", "发送间隔(ms)"))
        self.loop_bu.setText(_translate("MainWindow", "循环发送"))
    def loop_send_data(self):
        if self.flag and self.comboBox.currentIndex()==0:  #客户端发送
            self.thread_c.s.send(bytes(self.send_ms.toPlainText(), encoding='utf8'))
        elif self.flag and self.comboBox.currentIndex()==1:  #服务端发送
            self.thread_s.cli.send(bytes(self.send_ms.toPlainText(), encoding='utf8'))
    def loop_send(self):
        print(self.loop_bu.isChecked())
        if self.loop_bu.isChecked():
            self.timer = QTimer()  # 初始化定时器
            self.timer.timeout.connect(self.loop_send_data)
            self.timer.start(int(self.time_bu.toPlainText()))  # 设置计时间隔并启动
        else:
            self.timer.stop()
    def send(self):   #点发送按钮
        if self.flag and self.comboBox.currentIndex()==0:  #客户端才可以发送+clien
            self.thread_c.s.send(bytes(self.send_ms.toPlainText(), encoding='utf8'))
        elif self.flag and self.comboBox.currentIndex()==1:  #服务端发送
            self.thread_s.cli.send(bytes(self.send_ms.toPlainText(), encoding='utf8'))
    def setcheck(self):
        if self.flag:  #从连接到断开
            if self.comboBox.currentIndex() == 0:  #断开客户端子线程
                print("关闭clien")
                self.thread_c.s.close()
                self.thread_c.quit()
            if self.comboBox.currentIndex() == 1:  #断开服务器子线程
                print("关闭server")
                try:
                    self.thread_s.cli.close()  #若没有客户端连服务器就关闭，将产生异常
                except:
                    self.thread_s.s.close()
                self.thread_s.quit()

        else:
            if self.comboBox.currentIndex() == 1:  #开启服务器子线程
                self.thread_s=Thread_1(self.show_ip.toPlainText(),self.show_port.toPlainText())
                self.thread_s.signal.connect(self.callback)  #子线程连接父线程的回调函数
                self.thread_s.start()
            if self.comboBox.currentIndex() == 0:  #开启客户端子线程
                self.thread_c=Thread_2(self.show_ip.toPlainText(),self.show_port.toPlainText())
                self.thread_c.signal.connect(self.callback)  #子线程连接父线程的回调函数
                self.thread_c.start()
        self.flag = (1 ^ self.flag)  #按一下改变一下状态
    def get_mode(self):    #如果flag为真那么肯定开启了一个子线程，为假不用管
        if self.flag:  #从连接到断开
            if self.comboBox.currentIndex() == 0:  #断开服务器子线程
                self.thread_s.cli.close()
                self.thread_s.quit()

            if self.comboBox.currentIndex() == 1:  #断开客户端子线程
                self.thread_c.s.close()
                self.thread_c.quit()
        self.radioButton.setChecked(False)  #按钮变成未选定，同时变未连接标志位
        self.flag=0
    def callback(self,mes):  #接受子线程数据,判断是否继续进行子线程
        self.window.append("【server:】时间：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\t" + self.show_ip.toPlainText() + ":" + self.show_port.toPlainText())
        self.window.append(mes)
        """if mes=="配置不正确":    #服务器出现连接异常进行的处理
            print(self.thread_c.isRunning())
            if self.comboBox.currentIndex() == 0 and self.thread_c.isRunning(): #clien
                print("c")
                self.thread_c.s.close()
                self.thread_c.quit()
            elif self.comboBox.currentIndex() == 1 and self.thread_s.isRunning():
                print("s")
                self.thread_s.cli.close()  #server
                self.thread_s.quit()"""
        if mes=="配置不正确":
            print(mes)
            self.flag=0
            self.radioButton.setChecked(False)
    def clear(self):  #清屏
        self.window.setText("")
    def write_ip(self):   #获取ip+填入
        ss=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))  #通过连接获取本机ip
        ip = ss.getsockname()[0]
        ss.close() #关闭套接字连接
        self.show_ip.setPlainText(str(ip)) #把主机ip展示在输入ip的窗口