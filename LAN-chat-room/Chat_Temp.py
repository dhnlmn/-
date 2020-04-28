# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtCore import QThread,pyqtSignal
import  socket
import  json

class Thread(QThread):
    signal=pyqtSignal(dict)
    def __init__(self,_ip,_port,_s_IP):
        super().__init__()
        self.ip=_ip   #客户端ip
        self.port=_port  #端口
        self.s_IP=_s_IP  #服务器ip
        print(1)
    def run(self):
        try:
            self.connect()
            print("连接成功")
            while True:
                self.data, self.addr = self.s.recvfrom(1024)
                #print(addr, data)
                #将bytes类型转换成str
                self.data = self.data.decode()
                if self.data=="签到":
                    self.s.sendto(b'1', (self.s_IP, int(self.port))) #签到了回复1
                    print("已经签到")
                    continue
                #将字符串转换成dict
                self.dict = json.loads(self.data)
                print(self.dict)
                if len(self.dict):  #不是签到消息就emit
                    self.signal.emit(self.dict)

        except:
            print("连接失败")
    def connect(self):
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        #设置可以广播
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.s.bind((self.ip, int(self.port)))
        self.s.sendto(b'hello', (self.s_IP, int(self.port)))
class Ui_MainWindow(object):
    def __init__(self):
        self.land_flag=1   #初始1，可以登陆，锁一次登陆
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.show_all_Q = QtWidgets.QTextEdit(self.centralwidget)
        self.show_all_Q.setGeometry(QtCore.QRect(30, 40, 391, 461))
        self.show_all_Q.setObjectName("show_all_Q")
        self.mes_show_Q = QtWidgets.QTextEdit(self.centralwidget)
        self.mes_show_Q.setGeometry(QtCore.QRect(40, 520, 301, 61))
        self.mes_show_Q.setObjectName("mes_show_Q")
        self.send_mes_bu = QtWidgets.QPushButton(self.centralwidget)
        self.send_mes_bu.setGeometry(QtCore.QRect(360, 530, 93, 51))
        self.send_mes_bu.setObjectName("send_mes_bu")
        self.Land_bu = QtWidgets.QPushButton(self.centralwidget)
        self.Land_bu.setGeometry(QtCore.QRect(360, 670, 93, 28))
        self.Land_bu.setObjectName("Land_bu")
        self.ip_show_Q = QtWidgets.QTextEdit(self.centralwidget)
        self.ip_show_Q.setGeometry(QtCore.QRect(53, 666, 261, 41))
        self.ip_show_Q.setObjectName("ip_show_Q")
        self.ip_show_Q.setText("192.168.0.103")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 20, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(630, 20, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(340, 0, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.people_show_Q = QtWidgets.QTextEdit(self.centralwidget)
        self.people_show_Q.setGeometry(QtCore.QRect(530, 40, 261, 461))
        self.people_show_Q.setObjectName("people_show_Q")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(550, 560, 72, 15))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(690, 560, 81, 20))
        self.label_5.setObjectName("label_5")
        self.server_port = QtWidgets.QTextEdit(self.centralwidget)
        self.server_port.setGeometry(QtCore.QRect(690, 590, 81, 31))
        self.server_port.setObjectName("server_port")
        self.server_port.setText("8888")
        self.server_ip = QtWidgets.QTextEdit(self.centralwidget)
        self.server_ip.setGeometry(QtCore.QRect(510, 590, 161, 31))
        self.server_ip.setObjectName("server_ip")
        self.server_ip.setText("192.168.0.105")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Land_bu.clicked.connect(self.land)
        self.send_mes_bu.clicked.connect(self.Send)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.send_mes_bu.setText(_translate("MainWindow", "发送"))
        self.Land_bu.setText(_translate("MainWindow", "登陆"))
        self.label.setText(_translate("MainWindow", "消息显示"))
        self.label_2.setText(_translate("MainWindow", "在线成员"))
        self.label_3.setText(_translate("MainWindow", "简易聊天室"))
        self.label_4.setText(_translate("MainWindow", "服务器ip"))
        self.label_5.setText(_translate("MainWindow", "服务器port"))

    def land(self):
        if self.land_flag:   #防止二次登陆，二次开线程
            self.lan_flag=0
            self.ip=self.ip_show_Q.toPlainText()    #自身ip
            self.port=self.server_port.toPlainText()   #port
            self.serverIP=self.server_ip.toPlainText()   #服务器ip
            print(self.ip)
            self.thread=Thread(self.ip,self.port,self.serverIP)   #开启客户端连接线程
            self.thread.signal.connect(self.callback)
            self.thread.start()
    def callback(self,data):   #回调函数处理客户端收到的信息，根据数据头类型区分
        if data["type"]=="member":   #添加成员
            self.people_show_Q.append(str(data["addr"]))
        elif data["type"]=="data":   #聊天信息
            self.show_all_Q.append(str(data["addr"]))
            self.show_all_Q.append(str(data["data"]))
        elif data["type"]=="updata":  #更新成员信息
            self.people_show_Q.setText("")   #清空
            for i in data["data"]:
                self.people_show_Q.append(str(i))
    def Send(self):     #发信息
        self.mes=self.mes_show_Q.toPlainText()
        self.thread.s.sendto(bytes(self.mes,encoding="utf8"),(self.serverIP, int(self.port)))
        #发信息给服务端，让服务端广播给各个客户端