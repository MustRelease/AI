from controller import Controller
import requests
import ast

controller = Controller()

class Retriever:
	def __init__(self):
		self.r_message = "<연아의 기억>\n"
		self.r_message += "index text priority\n"

	def retrieve_memory_system(self, data):
		userId = data.userId
		response = controller.load_memory(data.content, userId)
		id_list = list(map(lambda x : x["ids"], response))
		for data in response:
			text = str(data["ids"]) + " "
			text += data["observation"] + " "
			text += str(round(data["priority"], 2)) + "\n"
			#reflect 근거 문장 불러오기
			if data["reasonIds"] != "null":
				reason_list = ast.literal_eval(data["reasonIds"])
				for id in reason_list:
					if id not in id_list:
						r = controller.load_memory_id(id, userId)[0]
						text += str(id) + " "
						text += r["observation"] + " "
						text += str(round(r["importance"], 2)) + "\n"
						id_list.append(id)
			self.r_message += text
		self.r_message += "\n"
		return self.r_message

	def retrieve_buffer(self, userId):
		text = ""
		response = controller.load_buffer(userId)
		for data in response:
			text = text + data["observation"] + "\n"
		return text
