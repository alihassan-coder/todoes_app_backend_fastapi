from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import datetime
from pydantic import BaseModel

import os

CRUAD_routes = APIRouter()

load_dotenv()

class AddTodos(BaseModel):
    title: str
    description: str
    status: str


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
db = client["Todos"]

@CRUAD_routes.get("/")
def read_root():
    try:
        return {
            "message": "CRUAD is running successfully",
            "status": 200,
            "data": [],
        }
    except Exception as e:
        return {
            "message": str(e),
            "status": 500,
            "data": [],
        }

# this is for read all todos in database
@CRUAD_routes.get("/todos")
def read_todos():
    try:
        todos = db.AddTodos.find()
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

# this is for read a single todo by id in database
@CRUAD_routes.get("/onetodos/{id}")
def read_single_todos(id: str):
    try:
        id = id.strip() 

        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        todo_id = ObjectId(id)
        todo = db.AddTodos.find_one({"_id": todo_id})

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        return {
            "data": {
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "status": todo["status"],
                "created_at": todo["created_at"],
            },
            "error": None,
            "message": "Todo read successfully",
            "status": "success"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {
            "data": [],
            "error": "Error reading todo",
            "message": str(e),
            "status": "failed"
        }

# this is for create a todo in database using bodyparams
@CRUAD_routes.post("/addtodos")
def add_todos(todo: AddTodos):
    try:
        todo_dict = {
            "title": todo.title,
            "description": todo.description,
            "status": todo.status,
            "created_at": datetime.datetime.now(),
        }
        result = db.AddTodos.insert_one(todo_dict)

        # Ensure the inserted ID is converted to a string
        todo_dict["_id"] = str(result.inserted_id)

        return {
            "data": todo_dict,
            "error": None,
            "message": "Todo added successfully",
            "status": "success"
        }
    except Exception as e:
        return {
            "data": [],
            "error": "Error adding todo",
            "message": str(e),
            "status": "failed"
        }

# delete a todo by id in database by id
@CRUAD_routes.delete("/deletetodos/{id}")
def delete_todos(id: str):
    try:
        id = id.strip()

        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        todo_id = ObjectId(id)
        todo = db.AddTodos.find_one({"_id": todo_id})

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        db.AddTodos.delete_one({"_id": todo_id})

        return {
            "data": [],
            "error": None,
            "message": "Todo deleted successfully",
            "status": "success"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {
            "data": [],
            "error": "Error deleting todo",
            "message": str(e),
            "status": "failed"
        }

# update a todo by id in database by id
@CRUAD_routes.put("/updatetodos/{id}")
def update_todos(id: str, todo: AddTodos):
    try:
        id = id.strip()

        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        todo_id = ObjectId(id)
        existing_todo = db.AddTodos.find_one({"_id": todo_id})

        if not existing_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        db.AddTodos.update_one({"_id": todo_id}, {"$set": todo.dict()})

        return {
            "data": [],
            "error": None,
            "message": "Todo updated successfully",
            "status": "success"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {
            "data": [],
            "error": "Error updating todo",
            "message": str(e),
            "status": "failed"
        }
    
    