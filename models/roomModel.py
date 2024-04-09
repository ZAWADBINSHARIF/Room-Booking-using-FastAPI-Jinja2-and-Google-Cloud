from pydantic import BaseModel


class PostRoomModel(BaseModel):
    user_id: str
    name: str
    location: str