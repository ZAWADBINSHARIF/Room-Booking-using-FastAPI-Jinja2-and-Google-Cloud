# external import
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


# internal import
from config.databaseConnection import db, firestore
from models.roomModel import PostRoomModel


RB = roomBooking = APIRouter(prefix="/room")


RB_ref = db.collection("RB")


@RB.get("/")
async def get():

    print("get")
    return {"msg": "get"}


@RB.post("/add")
async def add_single_room(formData: PostRoomModel):

    try:
        room = dict(formData)
        print(room)
        docs = RB_ref.document(formData.room_id).get()

        if docs.exists:
            return JSONResponse(
                content={"msg": "This room already was created"}, status_code=409
            )
        else:
            RB_ref.document(formData.room_id).set(room)

    except Exception as error:
        print("error")
        return {"error": error}

    return JSONResponse(content={"msg": "New room was added"}, status_code=201)
