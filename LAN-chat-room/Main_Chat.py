import sys
import sip
import Chat_Temp
from PyQt5.QtWidgets import (QApplication,QDialog,QMainWindow)

if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = QMainWindow()
    myUI = Chat_Temp.Ui_MainWindow()
    myUI.setupUi(myDlg)
    myDlg.show()
sys.exit(myapp.exec_())