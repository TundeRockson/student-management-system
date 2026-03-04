# Import Qt core helpers (like matching flags for searching table items).
from PyQt6.QtCore import Qt

# Import the PyQt widgets used to build the GUI.
# QApplication: starts the Qt app/event loop
# QMainWindow: main application window shell (menus, toolbars, status bar, central widget)
# QDialog / QMessageBox: popup windows for forms and confirmations
# Layouts (QVBoxLayout/QGridLayout): position widgets inside windows
# Inputs (QLineEdit/QComboBox): collect user text and selections
# Table widgets: show database rows in a grid
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QLabel, QGridLayout, QLineEdit,
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog,
    QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
)

# QAction/QIcon are used for menu and toolbar items with optional icons.
from PyQt6.QtGui import QAction, QIcon

# sys is used to start the Qt app with command line args and exit cleanly.
import sys

# sqlite3 provides a lightweight file-based database engine.
import sqlite3


# -----------------------------
# Database helper class
# -----------------------------
class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        # Store the SQLite database filename/path on the instance.
        # Keeping this here avoids repeating the file name throughout the app.
        self.database_file = database_file

    def connect(self):
        # Open a connection to the SQLite database file.
        # Returns a "connection" object that can execute SQL and create cursors.
        connection = sqlite3.connect(self.database_file)
        return connection


# -----------------------------
# Main application window
# -----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configure the main window title and minimum size.
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # --- Menu bar setup ---
        # Add top-level menus to the menu bar.
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # --- Actions (menu/toolbar commands) ---
        # QAction is a reusable "command" that can live in menus and toolbars.
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About App", self)

        # Some platforms (notably macOS) move certain menu items automatically.
        # Setting NoRole prevents Qt from relocating/renaming this action.
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_student_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

        # --- Table setup ---
        # QTableWidget will display rows from the "students" table in the database.
        self.table = QTableWidget()

        # Four columns match the expected database columns: id, name, course, mobile.
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))

        # Hide the vertical header to make the UI cleaner.
        self.table.verticalHeader().setVisible(False)

        # Put the table in the center of the main window.
        self.setCentralWidget(self.table)

        # --- Toolbar setup ---
        # Create a toolbar and add action buttons for quick access.
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # --- Status bar setup ---
        # Create a status bar at the bottom of the window.
        # This app uses the status bar to show Edit/Delete buttons when a row is selected.
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # When a table cell is clicked, show context actions (Edit/Delete) in the status bar.
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        # Create an "Edit Record" button that opens the EditDialog.
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        # Create a "Delete Record" button that opens the DeleteDialog.
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # Remove any previously added QPushButton widgets from the status bar.
        # findChildren(QPushButton) searches the widget tree under this window
        # and returns all QPushButton instances.
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        # Add the new buttons to the status bar.
        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def load_data(self):
        # Load all students from the database and display them in the table.
        # This is called on app startup and after inserts/updates/deletes.

        # Create a database connection (object creation + method call pattern).
        connection = DatabaseConnection().connect()

        # Execute a query that returns all rows in the students table.
        # sqlite3 connection objects can execute SQL directly.
        result = connection.execute("SELECT * FROM students")

        # Clear the table first to avoid duplicating rows.
        self.table.setRowCount(0)

        # Insert each database row into the QTableWidget.
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)

            # Each value in row_data becomes one table cell.
            for column_number, data in enumerate(row_data):
                self.table.setItem(
                    row_number,
                    column_number,
                    QTableWidgetItem(str(data))  # QTableWidgetItem expects strings
                )

        # Always close the connection when done.
        connection.close()

    # Each of these methods opens a dialog window that performs a specific action.
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()  # exec() blocks until the dialog is closed

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


# -----------------------------
# About dialog (simple info popup)
# -----------------------------
class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()

        # Configure the message box.
        self.setWindowTitle("About")

        # Display static "about" text.
        content = """
        Created by Tunde Rockson
        """
        self.setText(content)


# -----------------------------
# Edit dialog (update an existing student)
# -----------------------------
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Configure the dialog.
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Use a vertical layout: widgets are stacked top-to-bottom.
        layout = QVBoxLayout()

        # Identify which row is selected in the main table.
        index = main_window.table.currentRow()

        # Read the current values from the selected row so the form can be pre-filled.
        student_name = main_window.table.item(index, 1).text()

        # Store the selected student's ID for the UPDATE query.
        # Keeping this as self.student_id makes it available inside update_student().
        self.student_id = main_window.table.item(index, 0).text()

        # --- Name field ---
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # --- Course dropdown ---
        # Populate with a fixed list of courses and select the student's current course.
        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Physics", "Statistics", "Geography", "Computer Science"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # --- Mobile field ---
        mobile = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # --- Update button ---
        # Clicking Update triggers the SQL UPDATE and refreshes the table.
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        # Apply the layout to the dialog window.
        self.setLayout(layout)

    def update_student(self):
        # Update the selected student's record in the database.

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        # Parameterized query with ? placeholders prevents SQL injection
        # and handles quoting safely.
        cursor.execute(
            "UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
            (
                self.student_name.text(),
                self.course_name.itemText(self.course_name.currentIndex()),
                self.mobile.text(),
                self.student_id,
            )
        )

        # Commit makes the change permanent in the database file.
        connection.commit()

        # Clean up database resources.
        cursor.close()
        connection.close()

        # Refresh the main table UI so changes are visible immediately.
        main_window.load_data()


# -----------------------------
# Delete dialog (confirm and delete)
# -----------------------------
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Delete Student Data")

        # Use a grid layout to place label and buttons in rows/columns.
        layout = QGridLayout()

        confirmation = QLabel("Are you sure you want to delete this record?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        # Add widgets to the grid.
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        self.setLayout(layout)

        # If Yes is clicked, perform the delete action.
        yes.clicked.connect(self.delete_student)

        # If No is clicked, close.
        no.clicked.connect(self.close)

    def delete_student(self):
        # Delete the currently selected student record from the database.

        # Determine which row is selected and get its ID.
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        # Delete by ID using a parameterized query.
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()

        cursor.close()
        connection.close()

        # Refresh UI to remove the deleted row from the table.
        main_window.load_data()

        # Close the confirmation dialog.
        self.close()

        # Show a success message after deleting.
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()


# -----------------------------
# Insert dialog (add a new student)
# -----------------------------
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # --- Name field ---
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # --- Course dropdown ---
        self.course_name = QComboBox()
        courses = ["Physics", "Statistics", "Geography", "Computer Science"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # --- Mobile field ---
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # --- Submit button ---
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        # Insert a new student row into the database using values from the form.

        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        # Insert the new record using a parameterized query.
        cursor.execute(
            "INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
            (name, course, mobile)
        )

        connection.commit()
        cursor.close()
        connection.close()

        # Refresh UI so the new student appears in the table.
        main_window.load_data()


# -----------------------------
# Search dialog (highlight matching student)
# -----------------------------
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Input field for the name to search.
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Clicking Search runs the search_student method.
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        # Search the database for a student by exact name and highlight matches in the table.

        name = self.student_name.text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        # Run a SELECT query using a placeholder.
        # NOTE: The SQL keyword is typed as "WHere" in the original code.
        # SQLite is case-insensitive for keywords, so it often still works,
        # but correcting to "WHERE" is best practice.
        result = cursor.execute("SELECT * FROM students WHere name = ?", (name,))
        rows = list(result)

        # Print rows to the console (useful for debugging during development).
        print(rows)

        # findItems searches visible items in the table widget and returns matches.
        # MatchFixedString requires an exact match (no partial matches).
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)

        # Select the matching items in the table to highlight the result.
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


# -----------------------------
# Application startup
# -----------------------------
# Create the QApplication object (required for any PyQt app).
app = QApplication(sys.argv)

# Create and show the main window.
main_window = MainWindow()
main_window.show()

# Load the initial data from the database into the table.
main_window.load_data()

# Start the Qt event loop; sys.exit ensures a clean exit code is returned to the OS.
sys.exit(app.exec())