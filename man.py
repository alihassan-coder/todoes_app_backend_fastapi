from fastapi import FastAPI
from pymongo import MongoClient # type: ignore
from dotenv import load_dotenv # type: ignore

import os

app = FastAPI()
load_dotenv()

def get_db_client():
    try:
        client = MongoClient(os.getenv("db_URI"))
        return client
    except Exception as e:
        return {
            "message": str(e),
            "status": 500,
            "data": [],
        }

client = get_db_client()
db = client["AddTodos"]

@app.get("/")
def read_root():
    try:
        return {
            "message": "Server is running successfully",
            "status": 200,
            "data": [],
        }
    except Exception as e:
        return {
            "message": str(e),
            "status": 500,
            "data": [],
        }

@app.get("/todos")
def read_todos():
    try:
        todos = db.todos.find()
        listTodos = []
        for todo in todos:
            listTodos.append({
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "status": todo["status"],
                "created_at": todo["created_at"],
            })
        return {
            "data": listTodos,
            "error": None,
            "message": "Todos read successfully",
            "status": "success"
        }
    except Exception as e:
        print(f"Error reading todos: {e}")
        return {
            "data": [],
            "error": "Error reading todos",
            "message": str(e),
            "status": "failed"
        }