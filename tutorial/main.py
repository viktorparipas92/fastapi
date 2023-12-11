from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


fake_items_db = [
    {'item_name': 'Foo'},
    {'item_name': 'Bar'},
    {'item_name': 'Baz'},
]


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class ModelName(str, Enum):
    alex_net = 'alex_net'
    res_net = 'res_net'
    le_net = 'le_net'


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/items/')
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        item_dict['price_with_tax'] = item.price + item.tax

    return item_dict


@app.get('/items/{item_id}')
async def read_item(
    item_id: int,
    needy: str,
    query: Optional[str] = None,
    short: bool = False,
):
    item = {'item_id': item_id, 'needy': needy}
    if query:
        item['query'] = query

    if not short:
        item['description'] = (
            'This is an amazing item that has a long description'
        )

    return item


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    return {'item_id': item_id, **item.model_dump()}


@app.get('/users/me')
async def read_user_me():
    return {'user_id': 'the current user'}


@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {'user_id': user_id}


@app.get('/users/{user_id}/items/{item_id}')
async def read_user_item(
    user_id: int,
    item_id: int,
    query: Optional[str] = None,
    short: bool = False,
):
    item = {'item_id': item_id, 'owner_id': user_id}
    if query:
        item['query'] = query

    if not short:
        item['description'] = (
            'This is an amazing item that has a long description'
        )

    return item


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    model = {'model_name': model_name}
    if model_name is ModelName.alex_net:
        message = 'Deep Learning FTW!'
    elif model_name.value == 'lenet':
        message = 'LeCNN all the images'
    else:
        message = 'Have some residuals'

    model['message'] = message
    return model


@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {'file_path': file_path}
