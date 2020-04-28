import sys
import sip
import assi
from PyQt5.QtWidgets import (QApplication,QDialog,QMainWindow)

if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = QMainWindow()
    myUI = assi.Ui_MainWindow()
    myUI.setupUi(myDlg)
    myDlg.show()
sys.exit(myapp.exec_())