# FastAPI Article Management API

This is a REST API built with FastAPI to manage articles, allowing for CRUD operations. The application uses MySQL for logging user actions and Firebase Firestore for storing articles. Additionally, every action is logged in a MySQL database for auditing purposes.

## Features

- **Create articles**: Admin users can create new articles in Firebase Firestore.
- **Update articles**: Admin and editor users can update existing articles.
- **View articles**: Admin, editor, and viewer users can view articles.
- **Delete articles**: Only admin users can delete articles.
- **Logging**: Every action is logged in the MySQL database, storing information like API endpoint, HTTP method, status code, and the user ID.

## Prerequisites

Make sure you have the following installed:

- Python 3.7 or higher
- MySQL Database
- Firebase account with Firestore enabled
- A requirements.txt file has been provided which you use to install all dependencies ( pip install -r requirements.txt )

## File Structure

- **Main.py**: Stores all api endpoints and the logic for creating logs
- **models.py**: Stores SqlAlchemy models for User and BookLogs tables of sql workbench
- **mysql_workbench.py**: Establishes connection with out sql server
- **schemas.py**: Stores pydantic model to perform data validation on Articles
