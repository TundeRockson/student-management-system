# Student Management System (PyQt6 + SQLite)

## Overview

This project is a **desktop Student Management System** built using
**Python, PyQt6, and SQLite**.\
The application provides a graphical user interface that allows users to
manage student records stored in a local database.

The system demonstrates how Python can be used to build a **full desktop
CRUD application** that connects a graphical interface to a relational
database.

Users can:

-   Add new students
-   Edit existing student records
-   Delete student records
-   Search for students
-   View all records in a table-based interface

The project highlights how **object-oriented programming**, **GUI
development**, and **database interaction** can be combined to build a
practical application.

------------------------------------------------------------------------

## Features

### Student Table View

When the application starts, all student records stored in the SQLite
database are automatically loaded and displayed in a table inside the
main window.

### Add Student

The **Add Student** dialog allows a new student record to be inserted
into the database by providing:

-   Student name
-   Course
-   Mobile number

After submission, the table refreshes to display the newly added record.

### Edit Student

Selecting a student row allows the user to update that student's
information.\
The edit dialog is pre-populated with the current record values.

### Delete Student

Users can remove a student record from the database after confirming the
deletion.

### Search Student

The search dialog allows users to search for a student by name. Matching
entries are highlighted in the table.

### About Dialog

Displays information about the application creator.

------------------------------------------------------------------------

## Technologies Used

-   **Python**
-   **PyQt6** -- used to build the graphical user interface
-   **SQLite** -- lightweight relational database used for storing
    student records

------------------------------------------------------------------------

## Project Structure

    student-management-system/
    │
    ├── main.py
    ├── database.db
    ├── icons/
    │   ├── add.png
    │   └── search.png
    └── README.md

### Main Components

#### DatabaseConnection

Handles all database connections for the application.

Encapsulating database access in a class helps keep the database logic
separate from the user interface logic.

#### MainWindow

The main application window which contains:

-   Menu bar
-   Toolbar
-   Student table
-   Status bar
-   Event handlers for user actions

This class is responsible for loading and refreshing student data.

#### Dialog Classes

Each major operation is handled through a dedicated dialog window.

  Class          Responsibility
  -------------- ----------------------------------
  InsertDialog   Adds new student records
  EditDialog     Updates existing student records
  DeleteDialog   Confirms and deletes records
  SearchDialog   Searches for student names
  AboutDialog    Displays application information

------------------------------------------------------------------------

## Database Schema

The application uses a single SQLite table.

### students

  Column   Type      Description
  -------- --------- ----------------------
  id       INTEGER   Primary key
  name     TEXT      Student name
  course   TEXT      Course of study
  mobile   TEXT      Student phone number

The database is stored locally in the file:

    database.db

SQLite was chosen because it requires **no server setup** and integrates
directly with Python through the `sqlite3` module.

------------------------------------------------------------------------

## Application Architecture

The application follows a simple **separation of concerns design**:

  -----------------------------------------------------------------------
  Layer                               Responsibility
  ----------------------------------- -----------------------------------
  GUI Layer                           PyQt windows, dialogs, and user
                                      interaction

  Database Layer                      SQLite connection and queries

  Application Logic                   Methods that coordinate UI events
                                      and database operations
  -----------------------------------------------------------------------

Using classes helps organize responsibilities and keeps the codebase
easier to maintain and expand.

------------------------------------------------------------------------

## Running the Application

### Install dependencies

    pip install -r requirements.txt

### Run the program

    python main.py

The graphical interface will launch and load student records from the
database.

------------------------------------------------------------------------

## Learning Objectives

This project demonstrates:

-   Building desktop applications using **PyQt6**
-   Structuring programs using **object-oriented programming**
-   Implementing **CRUD operations**
-   Connecting a GUI application to a **database**
-   Organizing applications into reusable classes
-   Creating a complete end-to-end Python application

------------------------------------------------------------------------

## Author

Tunde Rockson
