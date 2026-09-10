from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TIME TRAVEL API")

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


class BookingRequest(BaseModel):
    booking_id: str


class ChangeBookingRequest(BaseModel):
    booking_id: str
    destination: str
    travel_year: int


class CancelBookingRequest(BaseModel):
    booking_id: str


class RefundRequest(BaseModel):
    booking_id: str


@app.get("/")
def home():
    return {"message": "TIME TRAVEL API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# Get booking - GET
@app.get("/bookings/{booking_id}")
def get_booking(booking_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = %s",
        (booking_id.upper(),)
    )

    booking = cursor.fetchone()

    cursor.close()
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


# Get booking - POST
@app.post("/bookings")
def get_booking_post(request: BookingRequest):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = %s",
        (request.booking_id.upper(),)
    )

    booking = cursor.fetchone()

    cursor.close()
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


# Change booking
@app.put("/bookings/{booking_id}")
def change_booking(
    booking_id: str,
    request: ChangeBookingRequest
):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if booking exists
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = %s",
        (booking_id.upper(),)
    )

    booking = cursor.fetchone()

    if booking is None:
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Update destination and travel year
    cursor.execute(
        """
        UPDATE bookings
        SET destination = %s, travel_year = %s
        WHERE booking_id = %s
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
        "SELECT * FROM bookings WHERE booking_id = %s",
        (booking_id.upper(),)
    )

    updated_booking = cursor.fetchone()

    cursor.close()
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


# Cancel booking
@app.put("/bookings/{booking_id}/cancel")
def cancel_booking(
    booking_id: str,
    request: CancelBookingRequest
):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if booking exists
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = %s",
        (booking_id.upper(),)
    )

    booking = cursor.fetchone()

    if booking is None:
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Cancel the booking
    cursor.execute(
        """
        UPDATE bookings
        SET status = %s
        WHERE booking_id = %s
        """,
        (
            "cancelled",
            booking_id.upper()
        )
    )

    conn.commit()

    # Get updated booking
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = %s",
        (booking_id.upper(),)
    )

    updated_booking = cursor.fetchone()

    cursor.close()
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


# Process refund
@app.put("/bookings/{booking_id}/refund")
def process_refund(
    booking_id: str,
    request: RefundRequest
):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if booking exists
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = %s",
        (booking_id.upper(),)
    )

    booking = cursor.fetchone()

    if booking is None:
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Check if booking is cancelled
    if booking[4].lower() != "cancelled":
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Booking must be cancelled before a refund can be processed"
        )

    # Process refund
    cursor.execute(
        """
        UPDATE bookings
        SET status = %s
        WHERE booking_id = %s
        """,
        (
            "refunded",
            booking_id.upper()
        )
    )

    conn.commit()

    # Get updated booking
    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = %s",
        (booking_id.upper(),)
    )

    updated_booking = cursor.fetchone()

    cursor.close()
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