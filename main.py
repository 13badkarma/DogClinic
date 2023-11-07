import time
from enum import Enum
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Any

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', summary='Root')
def root():
    # ваш код здесь
    return "string"


@app.post("/post", summary='Get Post')
def get_post() -> Timestamp:
    # append new element to the list
    post_db.append(Timestamp(id=len(post_db) + 1, timestamp=int(time.time())))
    # return last element
    return post_db[-1]


@app.get("/dog", response_model=list[Dog], summary='Get Dogs')
def get_dogs(kind: DogType) -> Any:
    res = [dog for index, dog in dogs_db.items() if dog.kind == kind]
    return res


@app.post("/dog", response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog) -> Dog:
    if dog.pk in [value.pk for key, value in dogs_db.items()]:
        raise HTTPException(status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                            detail=f"dog with such pk already exsists {dogs_db[dog.pk]}")
    dogs_db[dog.pk] = dog
    return dog


@app.post("/dog/{pk}", response_model=Dog, summary='Get Dog By Pk')
def get_dog_by_pk(pk: int) -> Dog:
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no such dog in db")
    return dogs_db[pk]


@app.patch("/dog/{pk}", response_model=Dog, summary='Update Dog')
def get_dog_by_pk(pk: int, dog: Dog) -> Dog:
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no such dog in db")
    dogs_db[pk] = dog
    return dogs_db[pk]


# uvicorn.run(app, port=8000)
