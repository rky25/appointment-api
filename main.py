from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware  # import CORS middleware

app = FastAPI()

# Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins, change this in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

booked_slots = {}

class AppointmentRequest(BaseModel):
    userName: str
    preferredDate: str  # format 'YYYY-MM-DD'
    preferredTime: str  # format 'HH:MM'

class AppointmentResponse(BaseModel):
    status: str
    confirmedDateTime: str
    message: str

@app.post("/book-appointment", response_model=AppointmentResponse)
def book_appointment(request: AppointmentRequest):
    date = request.preferredDate
    time = request.preferredTime
    key = f"{date} {time}"
    
    if key in booked_slots:
        next_available = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M") + timedelta(hours=1)
        return AppointmentResponse(
            status="Not Available",
            confirmedDateTime=next_available.strftime("%Y-%m-%d %H:%M"),
            message=f"Slot not available. Next available: {next_available.strftime('%Y-%m-%d %H:%M')}"
        )
    else:
        booked_slots[key] = request.userName
        return AppointmentResponse(
            status="Booked",
            confirmedDateTime=f"{date} {time}",
            message="Your appointment is confirmed."
        )
