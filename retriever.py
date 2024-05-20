from controller import Controller
import requests

controller = Controller()

class Retriever:
	def __init__(self):
		self.r_message = "<연아의 기억>\n"
		self.r_message += "index text priority\n"

	def retrieve_memory_system(self, data):
		response = controller.load_memory(data.content, data.userId)
		for data in response:
			text = str(data["ids"]) + " "
			text += data["observation"] + " "
			text += str(round(data["priority"], 2)) + "\n"
			self.r_message += text
		self.r_message += "\n"
		return self.r_message

	def retrieve_buffer(self, userId):
		text = ""
		response = controller.load_buffer(userId)
		for data in response:
			text = text + data["observation"] + "\n"
		return text
