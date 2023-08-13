from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox, QAction
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore
import sqlite3
import requests

width = 983
height = 544

# class for GUI window including all PyQt5 widgets
class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("GUI/08_taskify_v1.ui", self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.saveButton.clicked.connect(self.saveChanges)
        self.addButton.clicked.connect(self.addNewTask)
        self.deleteButton.clicked.connect(self.deleteSelectedTasks)
        self.setFixedWidth(width)
        self.setFixedHeight(height)

        # Connect the random quote button to the showRandomQuote method
        self.randomQuoteButton.clicked.connect(self.showRandomQuote)

    # calendar date function
    def calendarDateChanged(self):
        print("The calendar date was changed")
        selected_date = self.calendarWidget.selectedDate().toPyDate()
        print("Date selected:", selected_date)
        self.updateTaskList(selected_date)

    # updating the task list when new task is added
    def updateTaskList(self, date):
        self.tasksListWidget.clear()
        # importing database
        db = sqlite3.connect("data/taskify database.db")
        cursor = db.cursor()
        
        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
            self.tasksListWidget.addItem(item)

    
    # function for save button
    def saveChanges(self):
        # connecting the database
        db = sqlite3.connect("data/taskify database.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()
        # for loop that automatically sets the check button to be unchecked 
        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                # executing SQL using query by updating tasks in database
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        # commiting database
        db.commit()

        message_box = QMessageBox()
        message_box.setText("Changes Saved.")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()

    # New task function
    def addNewTask(self):
        db = sqlite3.connect("data/taskify database.db")
        cursor = db.cursor()
        # converting user input to string 
        newTask = str(self.taskLineEdit.text())
        # assigning specific date to the one selected in calendar widget
        date = self.calendarWidget.selectedDate().toPyDate()
        
        # query that adds new task into database under the specific column
        query = "INSERT or REPLACE INTO tasks(task, completed, date) VALUES (?,?,?)"
        # presetting the date completed column to 'NO'
        row = (newTask, "NO", date,)
        # executing the query
        cursor.execute(query, row)
        db.commit()
        self.updateTaskList(date)
        self.taskLineEdit.clear()
   

    # delete task function
    def deleteSelectedTasks(self):
        selected_items = self.tasksListWidget.selectedItems()
        if not selected_items:
            return

        date = self.calendarWidget.selectedDate().toPyDate()

        db = sqlite3.connect("data/taskify database.db")
        cursor = db.cursor()

        for item in selected_items:
            task = item.text()

            query = "DELETE FROM tasks WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()

        self.updateTaskList(date)

    # Randomised quote function
    def showRandomQuote(self):
        # Assigning API Link to response variable
        response = requests.get("https://zenquotes.io/api/quotes")
        if response.status_code == 200:
            quotes = response.json()
            if isinstance(quotes, list) and len(quotes) > 0:
                quote = quotes[0]
                author = quote["a"]
                content = quote["q"]
                self.quoteTextEdit.setPlainText(f"{content}\n\n- {author}")
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText("Failed to fetch random quote.")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
