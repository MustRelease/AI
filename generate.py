from openai import OpenAI
import os
from typing_extensions import override
from openai import AssistantEventHandler
from etc import load_dotenv

class EventHandler(AssistantEventHandler):
	@override
	def on_text_created(self, text) -> None:
		print(f"\nassistant > ", end="", flush=True)
	@override
	def on_text_delta(self, delta, snapshot):
		print(delta.value, end="", flush=True)

class Generater:
	def __init__(self):
		self.assistant_id = "asst_pkhPiEMEmYXXb65mRqIkzP6t"
		self.client = OpenAI(
      		api_key=load_dotenv(".env")
        )

	def set_instructions(self, instruction):
		my_updated_assistant = self.client.beta.assistants.update(
  			self.assistant_id,
  			instructions=instruction
		)
		print(my_updated_assistant)

	def set_assistant(self, character):
		my_assistant = client.beta.assistants.create(
		    instructions=character,
		    name="연아",
		    model="gpt-4o-2024-05-13",
		)
		return my_assistant.id

	def generate(self, query, assis_id):
		print(query)
		thread = self.client.beta.threads.create()
		message = self.client.beta.threads.messages.create(
  			thread_id=thread.id,
  			role="user",
  			content=query
		)
		response = ""
		with self.client.beta.threads.runs.stream(
			thread_id=thread.id,
			assistant_id=assis_id
		) as stream:
			for text in stream.text_deltas:
				print(text, end="")
				response += text
		message = self.client.beta.threads.messages.create(
  			thread_id=thread.id,
  			role="user",
  			content="명령 : 방금 너가 한 말에서 문맥에 맞지 않은 말이 있다면 고쳐서 형식은 그대로 다시 출력한다."
		)
		return response


