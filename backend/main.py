from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="TIME TRAVEL API")

DB_NAME = "time_travel.db"


class BookingRequest(BaseModel):
    booking_id: str


@app.get("/")
def home():
    return {"message": "TIME TRAVEL API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/bookings/{booking_id}")
def get_booking(booking_id: str):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = ?",
        (booking_id.upper(),)
    )

    booking = cursor.fetchone()
    conn.close()

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return {
        "booking_id": booking[0],
        "customer_name": booking[1],
        "destination": booking[2],
        "travel_year": booking[3],
        "status": booking[4],
        "price": booking[5]
    }





@app.post("/bookings")
def get_booking_post(request: BookingRequest):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = ?",
        (request.booking_id.upper(),)
    )

    booking = cursor.fetchone()
    conn.close()

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return {
        "booking_id": booking[0],
        "customer_name": booking[1],
        "destination": booking[2],
        "travel_year": booking[3],
        "status": booking[4],
        "price": booking[5]
    }

class ChangeBookingRequest(BaseModel):
    booking_id: str
    destination: str
    travel_year: int

class CancelBookingRequest(BaseModel):
    booking_id: str

class RefundRequest(BaseModel):
    booking_id: str


@app.put("/bookings/{booking_id}")
def change_booking(
    booking_id: str,
    request: ChangeBookingRequest
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if booking exists
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = ?",
        (booking_id.upper(),)
    )

    booking = cursor.fetchone()

    if booking is None:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Update destination and travel year
    cursor.execute(
        """
        UPDATE bookings
        SET destination = ?, travel_year = ?
        WHERE booking_id = ?
        """,
        (
            request.destination,
            request.travel_year,
            booking_id.upper()
        )
    )

    conn.commit()

    # Get updated booking
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = ?",
        (booking_id.upper(),)
    )

    updated_booking = cursor.fetchone()

    conn.close()

    return {
        "message": "Booking successfully changed",
        "booking_id": updated_booking[0],
        "customer_name": updated_booking[1],
        "destination": updated_booking[2],
        "travel_year": updated_booking[3],
        "status": updated_booking[4],
        "price": updated_booking[5]
    }


@app.put("/bookings/{booking_id}/cancel")
def cancel_booking(
    booking_id: str,
    request: CancelBookingRequest
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if booking exists
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = ?",
        (booking_id.upper(),)
    )

    booking = cursor.fetchone()

    if booking is None:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Cancel the booking
    cursor.execute(
        """
        UPDATE bookings
        SET status = ?
        WHERE booking_id = ?
        """,
        (
            "cancelled",
            booking_id.upper()
        )
    )

    conn.commit()

    # Get updated booking
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = ?",
        (booking_id.upper(),)
    )

    updated_booking = cursor.fetchone()

    conn.close()

    return {
        "message": "Booking successfully cancelled",
        "booking_id": updated_booking[0],
        "customer_name": updated_booking[1],
        "destination": updated_booking[2],
        "travel_year": updated_booking[3],
        "status": updated_booking[4],
        "price": updated_booking[5]
    }



@app.put("/bookings/{booking_id}/refund")
def process_refund(
    booking_id: str,
    request: RefundRequest
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if booking exists
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = ?",
        (booking_id.upper(),)
    )

    booking = cursor.fetchone()

    if booking is None:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Check if booking is cancelled
    if booking[4].lower() != "cancelled":
        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Booking must be cancelled before a refund can be processed"
        )

    # Process refund
    cursor.execute(
        """
        UPDATE bookings
        SET status = ?
        WHERE booking_id = ?
        """,
        (
            "refunded",
            booking_id.upper()
        )
    )

    conn.commit()

    # Get updated booking
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = ?",
        (booking_id.upper(),)
    )

    updated_booking = cursor.fetchone()

    conn.close()

    return {
        "message": "Refund successfully processed",
        "booking_id": updated_booking[0],
        "customer_name": updated_booking[1],
        "destination": updated_booking[2],
        "travel_year": updated_booking[3],
        "status": updated_booking[4],
        "refund_amount": updated_booking[5]
    }