from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

@app.get("structured_data/structured_company_data.json")
def get_summary():
    try:
        file_path = "/home/ubuntu/data/summary.json"
        with open(file_path, "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
