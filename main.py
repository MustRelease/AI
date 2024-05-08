from fastapi import FastAPI
from typing import List
import uvicorn
from pydantic import BaseModel


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
def recommand(data : Init):
    pass

@app.post('/memory/save')
def recommand(data : Memory):
    pass

@app.post('/response/generate')
def recommand(data : Memory):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app" , host="127.0.0.1", port=8000)
