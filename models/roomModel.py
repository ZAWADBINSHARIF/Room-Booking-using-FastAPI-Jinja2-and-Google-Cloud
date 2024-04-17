from pydantic import BaseModel


class PostRoomModel(BaseModel):
    user_id: str
    name: str
    location: str


class BookingRoomModel(BaseModel):
    room_id: str
    user_id: str
    from_date: str
    to_date: str
