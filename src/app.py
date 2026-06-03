"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

# Additional activities
# Sports-related
activities.update({
    "Soccer Team": {
        "description": "Competitive soccer team practicing drills and playing matches",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pick-up games and skills training for basketball enthusiasts",
        "schedule": "Tuesdays and Fridays, 5:00 PM - 7:00 PM",
        "max_participants": 15,
        "participants": ["chris@mergington.edu"]
    },

    # Artistic
    "Art Society": {
        "description": "Painting, drawing, and mixed-media workshops",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["linda@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater production, acting coaching, and stagecraft",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["sam@mergington.edu"]
    },

    # Intellectual
    "Science Olympiad": {
        "description": "Team-based STEM competitions and experimental challenges",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["nina@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice debates, public speaking, and competitive tournaments",
        "schedule": "Tuesdays, 6:00 PM - 7:30 PM",
        "max_participants": 16,
        "participants": ["oliver@mergington.edu"]
    }
})


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants/{participant_email}")
def remove_participant(activity_name: str, participant_email: str):
    """Remove a participant from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if participant_email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found for this activity")

    activity["participants"].remove(participant_email)
    return {"message": f"Removed {participant_email} from {activity_name}"}
