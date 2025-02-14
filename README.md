# To-Do App Backend

This is a To-Do app backend built using FastAPI and MongoDB Atlas. It provides a simple API to manage tasks, including adding, retrieving, updating, and deleting tasks.

## Features
- Create, Read, Update, and Delete (CRUD) operations for tasks
- Fast and efficient API using FastAPI
- MongoDB Atlas for cloud-based database storage
- Dependency management using Poetry

## Requirements
- Python 3.10+
- Poetry (for dependency management)
- MongoDB Atlas account

## Installation
```sh
# Clone the repository
git clone https://github.com/alihassan-coder/todoes_app_backend_fastapi.git

cd todo-backend

# Install dependencies using Poetry
poetry install
```

## Set up Environment Variables
Create a `.env` file in the root directory and add your MongoDB connection string:
```sh
db_URI= your db uri
```

## Running the Application
```sh
# Activate the virtual environment
poetry shell

# Start the FastAPI server
poetry run uvicorn main:app --reload
```

## API Documentation
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Author
Ali Hassan

