"""Taskify Welcome/Login/Signup""" # pylint: disable=E0611, I1101, C0103
import sys
import re
import sqlite3
import uuid
from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget

# Object-oriented programming
class WelcomeScreen(QDialog):
    """
    Represents the welcome, login, and signup screen.
    This defines thee GUI and functionality for the three screens.
    It handles user input for login and signup and provides methods for switching between screens.
    """
    def __init__(self):
        super().__init__()
        loadUi("GUI/10b_welcome_page.ui", self)
        self.login.clicked.connect(self.go_to_login)
        self.create.clicked.connect(self.go_to_createscreen)
        qpixmap = QPixmap("GUI/assets/taskify_logo.png")
        self.taskify_logo.setPixmap(qpixmap)

    def go_to_login(self):
        """
        Function to navigate to the login screen.
        """

        login = LoginScreen()
        # Adding to stackedwidget for multiple screens on top of each other
        widget.addWidget(login)
        # Adding a screen to the list by changing the index, +1 means moving forward in the index
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_signup(self):
        """
        Function to navigate to the signup screen.
        """

        signup = CreateScreen()
        # Adding to stackedwidget for multiple screens on top of each other
        widget.addWidget(signup)
        # Adding a screen to the list by changing the index, +1 means moving forward in the index
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_createscreen(self):
        """
        Function to navigate to the create screen.
        """
        create = CreateScreen()
        # Adding to stackedwidget for multiple screens on top of each other
        widget.addWidget(create)
        # Adding a screen to the list by changing the index, +1 means moving forward in the index
        widget.setCurrentIndex(widget.currentIndex() + 1)

class LoginScreen(QDialog):
    """
    Represents the user login screen.
    This class defines the GUI and functionality for the user login screen.
    """
    def __init__(self):
        super().__init__()
        loadUi("GUI/10b_user_login.ui", self)
        # Using a PyQt5 property to set the password with dots for user privacy
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        # Connect the login button click event to 'login_function'
        self.login_button.clicked.connect(self.login_function)
        self.redirect_login.linkActivated.connect(self.redirect_to_signup)
        qpixmap = QPixmap("GUI/assets/login_logo.png")
        self.login_logo.setPixmap(qpixmap)
        self.back_button.clicked.connect(self.go_to_welcomescreen)

    def go_to_welcomescreen(self):
        """
        Function to navigate to the welcome screen.
        """
        welcome_page = WelcomeScreen()
        # Adding to stackedwidget for multiple screens on top of each other
        widget.addWidget(welcome_page)
        # Adding a screen to the list by changing the index, +1 means moving forward in the index
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def redirect_to_signup(self, link):
        """        
        This method is called when a link is activated in the login screen.
        If the link is for the signup page, it switches to the signup screen.
        """
        if link == "signup_page":
            self.go_to_signup()

    def go_to_signup(self):
        """
        Function to navigate to the signup screen.
        """
        signup = CreateScreen()
        # Adding to stackedwidget for multiple screens on top of each other
        widget.addWidget(signup)
        # Adding a screen to the list by changing the index, +1 means moving forward in the index
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def is_valid_password(self, password):
        """
        Check if a password is valid.
        
        This method checks whether a password meets the specified criteria for validity.
        Checks password (string) and returns True/False (boolean)
        """
        # Check for length of at least 8 characters
        if len(password) < 8:
            return False

        # Check for at least one symbol and one capital letter
        symbol_pattern = r"[!@#$%^&*()\[\]{}|;:'\",.<>?/]"
        capital_letter_pattern = r"[A-Z]"

        if not re.search(symbol_pattern, password) or \
        not re.search(capital_letter_pattern, password):

            return False

        return True

    def login_function(self):
        """
        This method is called when the "Login" button is clicked. It retrieves user input,
        validates the password, and checks if the login details are correct.
        """
        user = self.username_edit.text().lower()  # Convert the input username to lowercase
        password = self.password_edit.text()

        if len(user) == 0 or len(password) == 0:
            self.error_field.setText("Please input all fields.")
        elif not self.is_valid_password(password):
            self.error_field.setText("Invalid Password")
        else:
            data_base = sqlite3.connect("data/taskify database.db")
            cursor = data_base.cursor()
            # Query checking if username = password to verify login
            query = "SELECT Password FROM login_info WHERE LOWER(Username) = ?"
            cursor.execute(query, (user,))
            result_pass = cursor.fetchone()
            # checking if details are correct
            if result_pass is not None and result_pass[0] == password:
                # if correct print this
                process = QProcess(self)

                # Set the program to execute as the Python interpreter
                process.setProgram("python")

                # Set the arguments to pass to the Python interpreter
                process.setArguments(["10_taskify_v3.py"])

                # Start the process
                process.start()

                self.error_field.setText("")
                # Generating a unique user ID
                user_id = str(uuid.uuid4())
                # Update the user ID in the database
                update_query = "UPDATE login_info SET user_id = ? WHERE Username = ?"
                cursor.execute(update_query, (user_id, user))
                data_base.commit()
                print("User ID:", user_id)
            else:
                # if incorrect print this
                if result_pass is None:
                    self.error_field.setText("Invalid username")
                else:
                    self.error_field.setText("Invalid password")
                    self.password_edit.clear()

class CreateScreen(QDialog):
    """
    This class defines the GUI and functionality for the user signup screen.
    It handles user input for signup and provides methods for navigating to other screens.
    """
    def __init__(self):
        super().__init__()
        loadUi("GUI/10b_user_signup.ui", self)
        self.redirect_signup.linkActivated.connect(self.redirect_to_login)
        qpixmap = QPixmap("GUI/assets/signup_logo.png")
        self.signup_logo.setPixmap(qpixmap)
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signup_function)
        self.back_button.clicked.connect(self.go_to_welcome)

    def go_to_welcome(self):
        """
        Function to navigate to the welcome screen.
        """
        welcome_page = WelcomeScreen()
        # Adding to stackedwidget for multiple screens on top of each other
        widget.addWidget(welcome_page)
        # Adding a screen to the list by changing the index, +1 means moving forward in the index
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def redirect_to_login(self, link):
        """
        Function to navigate to the login screen.
        """
        if link == "login_page":
            welcome.go_to_login()

    def is_valid_username(self, username):
        """
        Check if a username is valid.
        This method checks whether a username meets the specified criteria for validation.
        """
        return 3 <= len(username) <= 15

    def is_valid_password(self, password):
        """
        Check if a password is valid.
        This method checks whether a password meets the specified criteria for validation.
        """
        # Check for length of at least 8 characters
        if len(password) < 8:
            return False

        # Check for at least one symbol and one capital letter
        symbol_pattern = r"[!@#$%^&*()\[\]{}|;:'\",.<>?/]"
        capital_letter_pattern = r"[A-Z]"

        if not re.search(symbol_pattern, password) or \
        not re.search(capital_letter_pattern, password):
            return False

        return True

    def signup_function(self):
        """
        This method is called when the "Signup" button is clicked. It retrieves user input,
        validates the inputs, and creates a new user account if the inputs are valid.
        """
        user = self.username_field.text()

        # Check if the username contains only numbers
        if user.isdigit():
            self.error.setText("Username must be supported by letters.")
            return

        password = self.password_field.text()
        confirm_password = self.confirmpassword_field.text()

        if len(user) == 0 or len(password) == 0 or len(confirm_password) == 0:
            self.error.setText("Please fill all inputs.")
        elif not self.is_valid_username(user):
            self.error.setText("Username should be between 3 and 15 characters long.")
        elif not self.is_valid_password(password):
            self.error.setText("Password does not fill the requirements.")
        elif password != confirm_password:
            self.error.setText("Passwords do not match.")
        else:
            data_base = sqlite3.connect("data/taskify database.db")
            cursor = data_base.cursor()
            user_info = [user, password]
            cursor.execute('INSERT INTO login_info (Username, Password) VALUES (?,?)', user_info)
            data_base.commit()
            data_base.close()

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
widget.setFixedHeight(540)
widget.setFixedWidth(990)
widget.show()
sys.exit(app.exec_())
