from enum import Enum

from fastapi import FastAPI


app = FastAPI()


fake_items_db = [
    {'item_name': 'Foo'},
    {'item_name': 'Bar'},
    {'item_name': 'Baz'},
]


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


@app.get('/items/{item_id}')
async def read_item(item_id: int):
    return {'item_id': item_id}


@app.get('/users/me')
async def read_user_me():
    return {'user_id': 'the current user'}


@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {'user_id': user_id}


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
