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

class GenText(BaseModel):
    content : str
    regenerate : bool

@app.post('/memory/init')
def init(data : Init):
    code = controller.init_db(data.userId)
    if code != 200:
        raise HTTPException(status_code=code, detail="exist userId")
    code = controller.init_save(data)
    if code != 200:
        raise HTTPException(status_code=code, detail="memory save Error")


@app.post('/memory/save')
def save(data : List[Memory]):
    code = controller.save_all(data)
    if code != 200:
        raise HTTPException(status_code=code, detail="memory save Error")

@app.post('/response/generate')
def response(data : Memory):
    # 기억 생성
    message = ""
    generater = Generater()
    retriever = Retriever()
    message += retriever.retrieve_memory_system(data)
    message += "<현재 상황>\n"
    message += data.content
    message += "\nInstruct : 그래서 너는 기억과 현재 상황을 참고하여 지성에게 뭐라고 해야할까?"
    r = generater.generate(message)
    # 넘어온 기억 저장
    code = controller.save(data.userId, data.playTime, data.content, data.importance)
    if code != 200:
        raise HTTPException(status_code=code, detail="memory save Error")
    # 생성한 기억 저장
    code = controller.save(data.userId, data.playTime, '나는 ' + r + '라고 말했다.', 1.0)
    if code != 200:
        raise HTTPException(status_code=code, detail="memory save Error")
    # 반환값 생성
    dic = {
        "content" : r,
        "regenerate" : True
    }
    return dic

if __name__ == "__main__":
    uvicorn.run("main:app" , host="0.0.0.0", port=8080)
