from typing import Union

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from app.preprocess import preprocess

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
    
class File(BaseModel):
    content: str


@app.get("/hello")
def read_root():
    return {"Status": "Preprocessing server is up!"}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/preprocess/file")
async def create_upload_file(file: File):
    preprocessed = preprocess(file.content, md=False)
    return {"content": preprocessed}

@app.post("/preprocess/")
async def create_upload_file(file: File):
    preprocessed = preprocess(file.content, md=True)
    return {"content": preprocessed}