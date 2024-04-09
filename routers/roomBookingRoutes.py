# external import
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from datetime import datetime


# internal import
from config.databaseConnection import db, firestore
from models.roomModel import PostRoomModel


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


@RB.get("/")
async def get():
    return await get_All_Rooms()


@RB.post("/search-for-booking")
def search_for_booking_room(from_date: str, to_date: str):
    All_Rooms = []

    try:
        # Assuming you have a reference to your rooms collection (rooms_ref)
        docs = rooms_ref.stream()

        for doc in docs:
            roomData = doc.to_dict()
            daysArray = roomData.get("days")

            if daysArray != None:
                for day in daysArray:
                    dayData = day.get().to_dict()

                    Booked_Start_Date = dayData.get("from_date")
                    Booked_End_Date = dayData.get("to_date")

                    # Convert from_date and to_date to datetime objects
                    from_datetime_obj = datetime.strptime(
                        from_date, "%Y-%m-%d %H:%M:%S.%f%z"
                    )
                    to_datetime_obj = datetime.strptime(
                        to_date, "%Y-%m-%d %H:%M:%S.%f%z"
                    )

                    # Compare the datetime
                    if (
                        to_datetime_obj < Booked_Start_Date
                        or from_datetime_obj > Booked_End_Date
                    ):
                        # No overlap, add roomData to All_Rooms
                        All_Rooms.append(roomData)
                    else:
                        # Overlap, skip this room
                        break
            else:
                All_Rooms.append(roomData)

    except Exception as error:
        print(error)

    return {"All_Rooms": All_Rooms}


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
