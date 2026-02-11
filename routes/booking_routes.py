# routes/booking_routes.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from models import mongo as mongo_db

router = APIRouter()


class BookingCreate(BaseModel):
    booking_id: Optional[int] = None
    student_id: int
    teacher_id: int
    subject_id: int
    date_time: Optional[datetime] = None
    status: str = "pending"
    admin_notes: Optional[str] = ""


class BookingResponse(BookingCreate):
    pass


@router.post("/bookings")
def create_booking(booking: BookingCreate):
    # conflict check
    if booking.date_time is None:
        raise HTTPException(status_code=400, detail="date_time is required")
    existing = mongo_db.db.bookings.find_one({"teacher_id": booking.teacher_id, "date_time": booking.date_time})
    if existing:
        raise HTTPException(status_code=400, detail="Time slot already booked for this teacher.")

    booking_id = booking.booking_id
    if booking_id is None:
        cur = list(mongo_db.db.bookings.find({}, {"booking_id": 1}).sort("booking_id", -1).limit(1))
        booking_id = (cur[0].get("booking_id") if cur and cur[0].get("booking_id") else 1000) + 1

    doc = booking.dict()
    doc["booking_id"] = booking_id
    mongo_db.create_booking(doc)
    return {"message": "Booking created successfully", "booking_id": booking_id}


@router.get("/bookings", response_model=List[BookingResponse])
def get_all_bookings():
    bookings = [mongo_db.serialize_booking(b) for b in mongo_db.db.bookings.find()]
    for b in bookings:
        if isinstance(b.get("date_time"), datetime):
            b["date_time"] = b["date_time"].isoformat()
    return bookings


@router.post("/lessons")
def create_lesson(booking: BookingCreate):
    """Alias endpoint for creating a lesson (same as bookings)."""
    return create_booking(booking)


@router.get("/lessons", response_model=List[BookingResponse])
def get_all_lessons():
    """Alias to list lessons."""
    return get_all_bookings()


@router.get("/lessons/student/{student_id}", response_model=List[BookingResponse])
def get_lessons_for_student(student_id: int):
    """Alias to fetch lessons for student."""
    return get_bookings_for_student(student_id)


@router.delete("/lessons/{booking_id}")
def cancel_lesson(booking_id: int):
    """Alias to cancel a lesson."""
    return cancel_booking(booking_id)


@router.get("/bookings/student/{student_id}", response_model=List[BookingResponse])
def get_bookings_for_student(student_id: int):
    student_bookings = [mongo_db.serialize_booking(b) for b in mongo_db.db.bookings.find({"student_id": student_id})]
    if not student_bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this student.")
    for b in student_bookings:
        if isinstance(b.get("date_time"), datetime):
            b["date_time"] = b["date_time"].isoformat()
    return student_bookings


@router.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int):
    res = mongo_db.db.bookings.find_one_and_update({"booking_id": booking_id}, {"$set": {"status": "cancelled"}})
    if not res:
        raise HTTPException(status_code=404, detail="Booking not found.")
    return {"message": "Booking cancelled successfully."}
