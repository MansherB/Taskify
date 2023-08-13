import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sqlite3
from PyQt5.QtCore import QProcess

# Object-oriented programming
# Creating a class called 'WelcomeScreen'
class WelcomeScreen(QDialog):
    def __init__(root):
        # Initializes parent class
        super(WelcomeScreen, root).__init__()
        # Load the UI from the .ui file
        loadUi("GUI/01b_welcome_page.ui", root)
        # Connect the 'login' button click event to the 'gotologin' function
        root.login.clicked.connect(root.gotologin)
        root.create.clicked.connect(root.gotocreate)

    def gotologin(root):
        login = LoginScreen()
        # Adding to stackedwidget for multiple screens on top of each other
        widget.addWidget(login)
        # Adding a screen to the list by changing the index, +1 means moving forward in the index
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate(root):
        create = create_account_screen()
        # Adding to stackedwidget for multiple screens on top of each other
        widget.addWidget(create)
        # Adding a screen to the list by changing the index, +1 means moving forward in the index
        widget.setCurrentIndex(widget.currentIndex() + 1)

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
        process.setArguments(["decomposition/09_taskify_v1.py"])
            
            # Start the process
        process.start()
            
       
    
class create_account_screen(QDialog):
    def __init__(self):
        super(create_account_screen, self).__init__()
        loadUi("GUI/02_user_signup.ui", self)
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword_field.setEchoMode(QtWidgets.QLineEdit.Password)
        # if the signup button is clicked, connect to function name 'signup_function'
        self.signup.clicked.connect(self.signup_function)

    def signup_function(self):
        user = self.username_field.text().lower()  # Convert to lowercase
        password = self.password_field.text()
        confirm_password = self.confirmpassword_field.text()

        db = sqlite3.connect("data/taskify database.db")
        cursor = db.cursor()
        # creating a 2 value array to add new row in database columns
        user_info = [user, password]
        # inserting the values 'user' and 'password' into the table
        cursor.execute('INSERT INTO login_info (Username, Password) VALUES (?,?)', user_info)
        
        db.commit()
        db.close()

        redirect_to_login = LoginScreen()
        widget.addWidget(redirect_to_login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        

# Main
# Creating a QApplication to launch the app
app = QApplication(sys.argv)
welcome = WelcomeScreen()
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
