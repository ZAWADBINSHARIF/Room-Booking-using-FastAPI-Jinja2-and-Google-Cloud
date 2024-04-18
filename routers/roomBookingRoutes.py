# external import
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from datetime import datetime


# internal import
from config.databaseConnection import db, firestore
from models.roomModel import PostRoomModel, BookingRoomModel


RB = roomBooking = APIRouter(prefix="/room")


rooms_ref = db.collection("rooms")
days_ref = db.collection("days")
bookings_ref = db.collection("bookings")


async def get_All_Rooms():

    All_Rooms = []

    try:
        docs = rooms_ref.stream()

        for doc in docs:
            roomData = doc.to_dict()
            daysArray = roomData.get("days")

            if daysArray:
                All_days = []
                for day in daysArray:
                    dayData = day.get().to_dict()
                    booking = dayData.get("booking")

                    if booking:
                        bookingData = booking.get().to_dict()
                        dayData["booking"] = bookingData

                    All_days.append(dayData)

                roomData["days"] = All_days
                All_Rooms.append(roomData)
            else:
                All_Rooms.append(roomData)

    except Exception as error:
        print(error)

    return All_Rooms


def search_for_booking_room(from_date: int | None = None, to_date: int | None = None):

    All_Rooms = []

    if from_date is None or to_date is None:
        return All_Rooms

    try:
        # Assuming you have a reference to your rooms collection (rooms_ref)
        docs = rooms_ref.stream()

        for doc in docs:
            roomData = doc.to_dict()
            daysArray = roomData.get("days")

            if daysArray is not None:

                isRoomFree = True

                for day in daysArray:
                    dayData = day.get().to_dict()

                    if (
                        dayData.get("from_date") is not None
                        and dayData.get("to_date") is not None
                    ):

                        DB_Booked_Start_Date = int(
                            dayData.get("from_date").timestamp() * 1000
                        )
                        DB_Booked_End_Date = int(
                            dayData.get("to_date").timestamp() * 1000
                        )

                        # Compare the datetime
                        if (
                            to_date < DB_Booked_Start_Date
                            or from_date > DB_Booked_End_Date
                        ):
                            # No overlap, add roomData to All_Rooms

                            pass
                        else:
                            isRoomFree = False
                            break

                if isRoomFree:
                    All_Rooms.append(
                        {
                            "user_id": roomData.get("user_id"),
                            "name": roomData.get("name"),
                            "location": roomData.get("location"),
                        }
                    )

            else:
                All_Rooms.append(roomData)

    except Exception as error:
        print(error)

    return All_Rooms


@RB.get("/")
async def get():
    return await get_All_Rooms()


@RB.post("/search-for-booking")
async def free_room_searching(from_date: int, to_date: int):
    return await search_for_booking_room(from_date, to_date)


@RB.post("/add")
async def add_single_room(formData: PostRoomModel):

    try:
        room = dict(formData)

        docs = rooms_ref.document(formData.name).get()

        if docs.exists:
            return JSONResponse(
                content={"msg": "This room already was created"}, status_code=409
            )
        else:
            rooms_ref.document(formData.name).set(room)

    except Exception as error:
        print("error")
        return {"error": error}

    return JSONResponse(content={"msg": "New room was added"}, status_code=201)


@RB.post("/add-booking")
async def add_booking(formData: BookingRoomModel):

    try:
        start_date = datetime.strptime(formData.from_date, "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(formData.to_date, "%Y-%m-%dT%H:%M")

        bookings_document_ref = bookings_ref.document()
        days_document_ref = days_ref.document()
        rooms_document_ref = rooms_ref.document(formData.room_id)

        bookings_document_ref.set({"user_id": formData.user_id})
        days_document_ref.set(
            {
                "from_date": start_date,
                "to_date": end_date,
                "booking_id": bookings_document_ref,
            }
        )
        rooms_document_ref.update({"days": firestore.ArrayUnion([days_document_ref])})

    except Exception as e:
        print(e)
        return JSONResponse(content={"msg": "something was wrong"}, status_code=500)

    return JSONResponse(content={"msg": "Booking has been done"}, status_code=201)
