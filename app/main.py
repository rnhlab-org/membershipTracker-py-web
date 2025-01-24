# Import necessary modules for the web service
from fastapi import FastAPI, Form  # FastAPI framework for creating APIs and handling form submissions
from fastapi.responses import HTMLResponse  # Used to send HTML responses
from fastapi.staticfiles import StaticFiles  # Serves static files (CSS, JS)
from fastapi.templating import Jinja2Templates  # Template engine for rendering HTML
from starlette.requests import Request  # Represents incoming HTTP requests
import requests  # Library for making HTTP requests to the backend API
import os  # For fetching environment variables

# Define the application version dynamically from the environment variable
# This version is passed during the container build process
__version__ = os.getenv("APP_VERSION", "0.0.0")

# Initialize the FastAPI application
app = FastAPI()

# Define the directory for HTML templates
templates = Jinja2Templates(directory="templates")

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the root endpoint to serve the home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Fetches the list of members from the API service and renders them
    on the home page along with a form to add new members.
    """
    try:
        # Call the backend API service to fetch the members list
        response = requests.get("http://api-service.default.svc.cluster.local:8000/members", timeout=10)
        members = response.json() if response.status_code == 200 else []
    except Exception as e:
        # Handle any errors gracefully and log the issue
        members = []
        print(f"Error fetching members: {e}")

    # Render the home page template with the members data
    return templates.TemplateResponse("index.html", {"request": request, "members": members})

# Define an endpoint to handle form submissions for adding members
@app.post("/submit")
async def submit(name: str = Form(...), email: str = Form(...)):
    """
    Accepts form submissions for adding new members and sends the data
    to the backend API service.
    """
    try:
        # Send the new member data to the API service
        response = requests.post(
            "http://api-service.default.svc.cluster.local:8000/members",
            json={"name": name, "email": email},
            timeout=10  # Set a timeout of 10 seconds from sonarqube fix
        )
        return {"status": "success" if response.status_code == 200 else "error"}
    except Exception as e:
        # Log any errors and return a failure response
        print(f"Error submitting member: {e}")
        return {"status": "error"}

# Define an endpoint to fetch the current application version
@app.get("/version")
async def version():
    """
    Returns the current version of the application, fetched from the APP_VERSION environment variable.
    """
    return {"service": "membershipTracker-py-web", "version": __version__}