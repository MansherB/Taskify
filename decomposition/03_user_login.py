import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sqlite3
from PyQt5.QtCore import QProcess


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("GUI/03_user_login.ui", self)
        # Using a PyQt5 property to set the password with dots for user privacy
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        # Connect the login button click event to 'loginfunction'
        self.pushButton.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.lineEdit_1.text()
        password = self.lineEdit_2.text()

        db = sqlite3.connect("data/taskify database.db")
        cursor = db.cursor()
        
        process = QProcess(self)
        
            # Set the program to execute as the Python interpreter
        process.setProgram("python")
        
            # Set the arguments to pass to the Python interpreter
            # Opening main.py
        process.setArguments(["decomposition/09_taskify_1.py"])
            
            # Start the process
        process.start()
        
        

# Main
# Creating a QApplication to launch the app
app = QApplication(sys.argv)
welcome = LoginScreen()
# QStackedWidget to stack multiple screens on top of each other
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(544)
widget.setFixedWidth(983)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
