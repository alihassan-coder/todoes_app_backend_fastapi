from fastapi import FastAPI
from routes.todos_CRUAD_routes import CRUAD_routes

app = FastAPI()

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

app.include_router(CRUAD_routes, prefix="/CRUAD", tags=["CRUAD"])


