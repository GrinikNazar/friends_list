from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional, List
from db import friends_table
from aws_utils import save_file

app = FastAPI(title="Friends API")

app.mount("/media", StaticFiles(directory="./media"), name="media")


class Friend(BaseModel):
    id: str
    name: str
    profession: str
    profession_description: Optional[str] = None
    photo_url: str


class FriendCreate(BaseModel):
    name: str = Field(..., min_length=1)
    profession: str = Field(..., min_length=1)
    profession_description: Optional[str] = None


@app.post("/friends", response_model=Friend)
async def create_friend(
        name: str = Form(...),
        profession: str = Form(...),
        profession_description: Optional[str] = Form(None),
        photo: UploadFile = File(...)
):

    # Валідація
    friend_data = FriendCreate(
        name=name, profession=profession, profession_description=profession_description
    )

    photo_url = save_file(photo)

    friend = Friend(
        id=str(uuid4()),
        name=friend_data.name,
        profession=friend_data.profession,
        profession_description=friend_data.profession_description,
        photo_url=photo_url
    )

    friends_table.put_item(Item=friend.dict())
    return friend


@app.get("/friends", response_model=List[Friend])
def list_friends():
    result = friends_table.scan()
    return result.get("Items", [])


@app.get("/friends/{id}", response_model=Friend)
def get_friend(id: str):
    response = friends_table.get_item(Key={"id": id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Friend not found")
    return response["Item"]
