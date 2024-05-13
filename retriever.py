from controller import Controller
import requests

controller = Controller()

class Retriever:
	def __init__(self):
		self.r_message = "<연아의 기억>\n"
		self.r_message += "time text priority\n"

	def retrieve_memory_system(self, data):
		response = controller.load_memory(data.content, data.userId)
		for data in response:
			text = str(data["timestamp"] // 3600) + ":" + str((data["timestamp"] % 3600) // 60) + ":" + str(data["timestamp"] % 60) + " "
			text += data["observation"] + " "
			text += str(round(data["priority"], 2)) + "\n"
			self.r_message += text
		self.r_message += "\n"
		return self.r_message
