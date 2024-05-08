from fastapi import FastAPI
from typing import List
from typing import Union
import uvicorn
from pydantic import BaseModel
from generate import Generater
from retriever import Retriever

app = FastAPI()

class Data(BaseModel):
    content : str

class Init(BaseModel):
    userId : str
    data : Union[List[Data], None] = None
    character : str

class Memory(BaseModel):
	userId : str
	content : str
	playTime : str
	importance : float

@app.post('/memory/init')
def init(data : Init):
    pass

@app.post('/memory/save')
def save(data : Memory):
    pass

@app.post('/response/generate')
def response(data : Data):
    message = ""
    generater = Generater()
    retriever = Retriever()
    message += retriever.retrieve_memory_system()
    message += "<현재 상황>\n"
    message += data.content
    return generater.generate(message)


if __name__ == "__main__":
    uvicorn.run("main:app" , host="127.0.0.1", port=8000)
