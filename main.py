from fastapi import FastAPI, HTTPException
from typing import List
from typing import Union
import uvicorn
from pydantic import BaseModel
from generate import Generater
from retriever import Retriever
from controller import Controller
from reflect import Reflecter
from convert import Converter

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
	isDescription : bool | None = False
	count : int | None = 1

class Id(BaseModel):
    userId : str

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
    converter = Converter()
    if data.isDescription:
        data.content = converter.convert_description(data.content)
    code = controller.save(data.userId, data.playTime, data.content, data.importance)
    if code != 200:
        raise HTTPException(status_code=code, detail="memory save Error")

@app.post('/memories/save')
def save(data : List[Memory]):
    converter = Converter()
    for d in data:
        if d.isDescription:
            d.content = converter.convert_description(d.content)
    code = controller.save_all(data, True)
    if code != 200:
        raise HTTPException(status_code=code, detail="memory save Error")

@app.post('/response/generate')
def response(data : Memory):
    # 기억 생성
    message = ""
    generater = Generater()
    retriever = Retriever()
    message += retriever.retrieve_memory_system(data)
    message += "<이전 대화내용>\n"
    message += retriever.retrieve_buffer(data.userId)
    message += "\n<현재 상황>\n"
    message += data.content
    message += "\nInstruct : 그래서 너는 기억과 이전 대화내용을 참고하여 현재 상황에서 지성에게 뭐라고 해야할까?"
    message += ("\n" if data.count<3 else " 이제 대화를 마무리하는 말을 한다.\n")
    r = generater.generate(message)
    # 반환값 생성
    dic = {
        "content" : r,
        "regenerate" : True if data.count<3 else False
    }
    return dic

@app.post('/response/init')
def buffer_init(data : List[Memory]):
    code = controller.save_all(data, True)
    if code != 200:
        raise HTTPException(status_code=code, detail="memory save Error")


@app.post('/memory/reflect')
def reflect(data : Id):
    reflecter = Reflecter()
    #문맥에 맞게 중요도 부과
    buffer_memory = reflecter.get_importance(data.userId)
    controller.delete_buffer(data.userId)
    for d in buffer_memory:
        controller.save(data.userId, d["timestamp"], d["observation"], d["importance"])
    #Reflect 과정
    code = reflecter.reflect_anynum(data.userId)
    if code != 200:
        raise HTTPException(status_code=code, detail="Reflect Format Error : Try again")
    code = controller.relocate_buffer(data.userId)
    if code != 200:
        raise HTTPException(status_code=code, detail="move buffer Error")


if __name__ == "__main__":
    uvicorn.run("main:app" , host="0.0.0.0", port=8080)
