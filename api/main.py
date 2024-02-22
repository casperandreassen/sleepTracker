from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from enum import Enum
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()
app = FastAPI()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
USER_ID = os.getenv("USER_ID")

supabase: Client = create_client(url, key)
templates = Jinja2Templates(directory="templates")

class ActionEnum(str, Enum):
    sleep = "sleep"
    wake = "wake"

class Action(BaseModel):
    action: ActionEnum
    timestamp: datetime


@app.middleware("http")
async def validate_token(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token != USER_ID:
        return JSONResponse(
            status_code=401,
            content="Incorrect token",

        )
    try:
        response = await call_next(request)
        return response
    except HTTPException as e:
        return e



@app.post("/action")
async def post_action(action: Action):
    response = supabase.table("actions").insert({"action": action.action, "time": action.timestamp.isoformat(), "user_id": USER_ID}).execute()
    if response.data:
        return response.data
    else:
        return Exception("Could not insert.")


@app.delete("/action")
async def delete_last_action():
    data, count = supabase.table("actions").select("id").order("created_at").limit(1).execute()
    print(data)
    if len(data[1]) != 1:
        raise HTTPException(status_code=404)
    response = supabase.table("actions").delete().eq("id", data[1][0]["id"]).eq("user_id", USER_ID).execute()
    if len(response.data) == 1:
        return JSONResponse(status_code=204, content=response.data)
    else:
        raise HTTPException(status_code=500, detail="Could not delete item.")
    

@app.get("/actions")
async def get_last_actions(request: Request):
    data, count = supabase.table("actions").select("*").order("created_at").limit(5).execute()
    return templates.TemplateResponse("actions.html", {"request": request, "actions": data[1]})