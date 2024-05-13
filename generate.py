from openai import OpenAI
from dotenv import load_dotenv
import os
from typing_extensions import override
from openai import AssistantEventHandler

class EventHandler(AssistantEventHandler):
	@override
	def on_text_created(self, text) -> None:
		print(f"\nassistant > ", end="", flush=True)
	@override
	def on_text_delta(self, delta, snapshot):
		print(delta.value, end="", flush=True)


class Generater:
	def __init__(self):
		load_dotenv(override=True)
		self.assistant_id = "asst_pkhPiEMEmYXXb65mRqIkzP6t"
		self.client = OpenAI(
      		api_key=os.environ.get("OPENAI_API_KEY")
        )

	def generate(self, query):
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
			assistant_id=self.assistant_id,
			instructions="연아의 기억과 현재 상황을 참고하여 지성과 한 문장으로 대화해줘"
		) as stream:
			for text in stream.text_deltas:
				print(text, end="")
				response += text
		return response


