# Import necessary modules
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import requests

# Initialize FastAPI app
app = FastAPI()

# Set up templates directory for rendering HTML
templates = Jinja2Templates(directory="templates")

# Static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Endpoint to render the home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Fetch members from the API service
    response = requests.get("http://api-service.default.svc.cluster.local:8000/members")
    members = response.json() if response.status_code == 200 else []
    return templates.TemplateResponse("index.html", {"request": request, "members": members})

# Endpoint to handle form submissions
@app.post("/submit")
async def submit(name: str = Form(...), email: str = Form(...)):
    # Send data to the API service
    response = requests.post("http://api-service.default.svc.cluster.local:8000/members", json={"name": name, "email": email})
    return {"status": "success" if response.status_code == 200 else "error"}
