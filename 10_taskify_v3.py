"""Main Page"""  # pylint: disable=E0611, C0103, I1101
import sys
import sqlite3
import requests
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QTextCharFormat, QColor, QFontDatabase, QFont

# Setting Fixed Size
WIDTH_SIZE = 990
HEIGHT_SIZE = 550

# Class for GUI window including all PyQt5 widgets
class Window(QWidget):
    """
    The main GUI window class for Taskify
    handles the interaction between user interface and imports main widgets
    """
    def __init__(self):
        super().__init__()
        # exception handling
        try:
            loadUi("GUI/10_taskify_v3.ui", self)
        except FileNotFoundError as e:
            print("Error loading UI:", e)
        # importing all widgets, buttons, images and loading the GUI
        self.calendarWidget.selectionChanged.connect(self.calendar_date_changed)
        self.calendar_date_changed()
        self.save_button.clicked.connect(self.save_changes)
        self.addtask_button.clicked.connect(self.add_new_task)
        self.delete_button.clicked.connect(self.delete_selected_tasks)
        self.setFixedWidth(WIDTH_SIZE)
        self.setFixedHeight(HEIGHT_SIZE)
        qpixmap = QPixmap("GUI/assets/taskify_logo.png")
        self.logo_label.setPixmap(qpixmap)
        self.list_widget.itemChanged.connect(self.task_check_state_changed)
        self.get_quote.clicked.connect(self.show_random_quote)
        self.urgent_task.clicked.connect(self.change_selected_date_color)

        # Custom font import
        font_path = "font/brush script mt kursiv.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font_size = 14
        custom_font = QFont(font_family, font_size)
        self.quoteTextEdit.setFont(custom_font)

    def change_selected_date_color(self):
        """
        Changes the selected date to a Orange colour.
        """
        selected_date = self.calendarWidget.selectedDate()
        date_format = QTextCharFormat()
        # Set the colour for urgent tasks
        date_color = QColor(255, 116, 62)
        date_format.setBackground(date_color)
        self.calendarWidget.setDateTextFormat(selected_date, date_format)


    def task_check_state_changed(self, item):
        """
        Handles the check state changed signal for a task
        This function is called when the check state of a task item changes.
        It updates the calendar date format based on the checked items.
        """
        # Get the selected date from the calendar widget
        date = self.calendarWidget.selectedDate()
        # Create a QTextCharFormat object to modify date formatting
        date_format = QTextCharFormat()

        # Check if all items are checked
        all_checked = all(
        item.checkState() == QtCore.Qt.Checked
        for item in self.list_widget.findItems("", QtCore.Qt.MatchContains)
        )
        # If all tasks are checked, clear the background formatting
        if all_checked:
            date_format.clearBackground()
        else:
            # Set the background color to yellow if not all tasks are checked
            date_color = QColor(255, 255, 0)
            date_format.setBackground(date_color)
        # Applying the modified date to the selected date on the calendar widget
        self.calendarWidget.setDateTextFormat(date, date_format)

    def calendar_date_changed(self):
        """
    This function is called whenever the user selects a new date in the calendar.
    It retrieves the selected date and updates the task list to display tasks
    associated with the selected date.
    """
        selected_date = self.calendarWidget.selectedDate().toPyDate()
        self.update_task_list(selected_date)

    def update_task_list(self, date):
        """
    This function queries the database for tasks associated with the provided date.
    It then populates the task list widget with the retrieved tasks, displaying
    their titles and completion status.
    """
        self.list_widget.clear()
        data_base = sqlite3.connect("data/taskify database.db")
        cursor = data_base.cursor()

        # Query to retrieve tasks and their completion status for the provided date
        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        # Iterating through the retrieved tasks and adding them to the tasks list widget
        results = cursor.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            # Setting the check state based on the completion status of the task
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
            # Add the task item to the tasks list widget
            self.list_widget.addItem(item)

    def save_changes(self):
        """
    Save the changes made to task completion status.
    This function iterates through the list of tasks, retrieves their titles
    and completion status, and updates the database accordingly.
    """
        # Connect to the SQLite database file
        data_base = sqlite3.connect("data/taskify database.db")
        cursor = data_base.cursor()
        # Get the selected date from the calendar widget
        date = self.calendarWidget.selectedDate().toPyDate()

        # Iterate through each task item in the tasks list widget
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            task = item.text()
            # Determine the completion status of the task
            if item.checkState() == QtCore.Qt.Checked:
                completed = "YES"
            else:
                completed = "NO"

            # Create a unique task ID using the task title and the selected date
            task_id = f"{task}_{date}"
            # Define the SQL query for inserting or replacing task data in the database
            query = (
            "INSERT OR REPLACE INTO tasks(task_id, task, completed, date) "
            "VALUES (?, ?, ?, ?)"
            )
            row = (task_id, task, completed, date)
            # Execute the SQL query and commit changes to the database
            cursor.execute(query, row)
            data_base.commit()

        # Display a message box indicating that changes have been saved
        message_box = QMessageBox()
        message_box.setText("Changes Saved.")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()

    def add_new_task(self):
        """
        Add a new task to the entry list.

        This function adds a new task to the task list for the selected date. The task
        is retrieved from the text input field. The task is associated with the selected
        date and unchecked by default.
        """
        data_base = sqlite3.connect("data/taskify database.db")
        cursor = data_base.cursor()
        # Get the new task from the text input field and strip any leading/trailing whitespace
        new_task = str(self.taskLineEdit.text()).strip()
        # If the new task is empty, display a message box and return without adding it
        if not new_task:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText("Please enter a task.")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
            return

        # Check if the new task exceeds the maximum allowed length
        if len(new_task) > 15:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText("Task is too long. Maximum 15 characters allowed.")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
            return

        # Get the selected date from the calendar widget
        date = self.calendarWidget.selectedDate().toPyDate()

        # Create a unique task ID
        task_id = f"{new_task}_{date}"
        # Defining the SQL query
        query = (
            "INSERT OR REPLACE INTO tasks(task_id, task, completed, date) "
            "VALUES (?, ?, 'NO', ?)"
        )
        row = (task_id, new_task, date)
        cursor.execute(query, row)
        data_base.commit()
        # Update the task list to display the newly added task
        self.update_task_list(date)
        # Clear the text input field
        self.taskLineEdit.clear()

        # Highlight the selected date with a yellow background in the calendar widget
        calendar_date = self.calendarWidget.selectedDate()
        date_color = QColor(255, 255, 0)
        date_format = QTextCharFormat()
        date_format.setBackground(date_color)
        self.calendarWidget.setDateTextFormat(calendar_date, date_format)

    def delete_selected_tasks(self):
        """
        This function deletes tasks that have been selected by the user from the task list
        for the currently selected date.
        """
        # Get a list of selected task items from the task list widget
        selected_items = self.list_widget.selectedItems()
        # If no items are selected, display a message box and return without performing any deletion
        if not selected_items:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText("Please select a task to delete.")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
            return

        date = self.calendarWidget.selectedDate().toPyDate()
        data_base = sqlite3.connect("data/taskify database.db")
        cursor = data_base.cursor()

        # Iterate through the selected task items and delete them from the database
        for item in selected_items:
            task = item.text()

            # SQL query to delete a task based on its title and date
            query = "DELETE FROM tasks WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        data_base.commit()

        # Clear any background formatting for the selected date in the calendar widget
        calendar_date = self.calendarWidget.selectedDate()
        date_format = QTextCharFormat()
        date_format.clearBackground()
        self.calendarWidget.setDateTextFormat(calendar_date, date_format)
        # Update the task list
        self.update_task_list(date)


    def show_random_quote(self):
        """
    Display a random quote in the quote text area.

    This function sends a request to the ZenQuotes API to fetch a random quote.
    If a successful response is received, the function extracts the quote content
    from the link and then displays.
    """
        # Sending a GET request to the ZenQuotes API to fetch a random quote
        response = requests.get("https://zenquotes.io/api/quotes", timeout=10)
        try:
            response = requests.get("https://zenquotes.io/api/quotes", timeout=10)
            response.raise_for_status()  # Raise an exception if no response from server
            quotes = response.json()
        # Handle the request error, e.g., show an error message to the user
        except requests.RequestException as e:
            print("Server Request Error. Please try again later.", e)
        # Check if the response status code is successful
        if response.status_code == 200:
            # Retrieving the list of quotes
            quotes = response.json()
            # Check if the quotes list is not empty
            if isinstance(quotes, list) and len(quotes) > 0:
                # Extract the first quote from the list
                quote = quotes[0]
                # Extract the author of the quote
                author = quote["a"]
                # Extract the content
                content = quote["q"]
                # Display the quote content along with the author in the text field
                self.quoteTextEdit.setPlainText(f"{content}\n\n- {author}")
        else:
            # If the API request was not successful, show an error message
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText("Unable to display quote. Please try again later.")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()

if __name__ == "__main__":
    # QApplication instance used to manage the GUI application
    app = QApplication(sys.argv)
    # Representing the main GUI window
    window = Window()
    # Displaying the window
    window.show()
    # Start the application's event loop, handling user input
    sys.exit(app.exec_())
