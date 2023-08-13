import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget

class LoginScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("GUI/03b_user_login.ui", self)
        # Using a PyQt5 property to set the password with dots for user privacy
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        # Connect the login button click event to 'login_function'
        self.login_button.clicked.connect(self.login_function)

    def is_valid_password(self, password):
        pass

    def login_function(self):
        pass

# Main
# Creating a QApplication to launch the app
app = QApplication(sys.argv)
welcome = LoginScreen()
# QStackedWidget to stack multiple screens on top of each other
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(540)
widget.setFixedWidth(990)
widget.show()
sys.exit(app.exec_())
