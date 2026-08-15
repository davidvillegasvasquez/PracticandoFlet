#Correr el servidor: uv run fastapi dev
#Ver la documentación automática e interactiva de tu api: http://127.0.0.1:8000/docs y la documentación alternativa: http://127.0.0.1:8000/redoc

from fastapi import FastAPI
#Aquí la variable app será una "instancia" de la clase FastAPI. Este será el punto principal de interacción para crear toda su API.
app = FastAPI()

@app.get("/")
async def root():
    return {"mensaje": "Hola mundo !!!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id+3}

from enum import Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


