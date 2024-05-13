from fastapi import FastAPI, HTTPException
from typing import List
from typing import Union
import uvicorn
from pydantic import BaseModel
from generate import Generater
from retriever import Retriever
from controller import Controller

app = FastAPI()
controller = Controller()

class Data(BaseModel):
    content : str

class Init(BaseModel):
    userId : str
    data : List[Data]
    character : str

class Memory(BaseModel):
	userId : str
	content : str
	playTime : str
	importance : float

@app.post('/memory/init')
def init(data : Init):
    code = controller.init_db(data.userId)
    if code != 200:
        raise HTTPException(status_code=code, detail="exist userId")
    code = controller.init_save(data)
    if code != 200:
        raise HTTPException(status_code=code, detail="memory save Error")


@app.post('/memory/save')
def save(data : Memory):
    code = controller.save(data)
    if code != 200:
        raise HTTPException(status_code=code, detail="memory save Error")

@app.post('/response/generate')
def response(data : Memory):
    message = ""
    generater = Generater()
    retriever = Retriever()
    message += retriever.retrieve_memory_system(data)
    message += "<현재 상황>\n"
    message += data.content
    return generater.generate(message)


if __name__ == "__main__":
    uvicorn.run("main:app" , host="127.0.0.1", port=8000)
