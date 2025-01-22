# Import necessary modules for the web service
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import requests  # Used to communicate with the API service
import os  # Used for fetching the version from environment variables

# Define the application version dynamically
__version__ = os.getenv("APP_VERSION", "0.0.0")

# Create a FastAPI application instance
app = FastAPI()

# Define the directory for templates (HTML files)
templates = Jinja2Templates(directory="templates")

# Mount the directory for static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the root route to render the home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page that fetches members from the API service
    and displays them along with a form for adding new members.
    """
    try:
        # Call the API service to fetch members
        response = requests.get("http://api-service.default.svc.cluster.local:8000/members")
        members = response.json() if response.status_code == 200 else []
    except Exception as e:
        members = []  # Handle errors gracefully
        print(f"Error fetching members: {e}")

    # Render the HTML template with the members data
    return templates.TemplateResponse("index.html", {"request": request, "members": members})

# Define a route to handle form submissions for adding new members
@app.post("/submit")
async def submit(name: str = Form(...), email: str = Form(...)):
    """
    Form submission handler that sends member data to the API service.
    """
    try:
        response = requests.post(
            "http://api-service.default.svc.cluster.local:8000/members",
            json={"name": name, "email": email},
        )
        return {"status": "success" if response.status_code == 200 else "error"}
    except Exception as e:
        print(f"Error submitting member: {e}")
        return {"status": "error"}

# Define a route to fetch the current version
@app.get("/version")
async def version():
    """
    Returns the current application version.
    """
    return {"service": "membershipTracker-py-web", "version": __version__}
