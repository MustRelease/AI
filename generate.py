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
		load_dotenv()
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
		with self.client.beta.threads.runs.stream(
		  	thread_id=thread.id,
		  	assistant_id=self.assistant_id,
			instructions="A의 기억과 현재 상황을 참고하여 주인공과 한 문장으로 대화해줘",
		  	event_handler=EventHandler(),
		) as stream:
			stream.until_done()


