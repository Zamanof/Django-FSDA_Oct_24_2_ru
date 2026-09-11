from typing import List, Optional

from fastapi import FastAPI
from models import CarRead, CarCreate
from car_repository_service import _create_car
from in_memory import _store

app = FastAPI()


@app.post('/cars', response_model=CarRead, status_code=201)
def create_car(payload: CarCreate):
    return _create_car(payload)


@app.get("/cars", response_model=List[CarRead], status_code=200)
def get_all_cars(
        model: Optional[str]=None,
        manufacturer: Optional[str]=None,
        limit: int = 100,
        offset: int=0):
    items = list(_store.values())
    if model:
        items = [c for c in items if model.lower() in c.model.lower()]
    if manufacturer:
        items = [c for c in items if manufacturer.lower() in c.manufacturer.lower()]

    offset = (offset -1) * limit
    print(items[offset:offset + limit])
    return items[offset:offset + limit]




