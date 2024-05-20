from openai import OpenAI
from dotenv import load_dotenv
import os

class Reflecter:
	def __init__(self):
		load_dotenv(override=True)
		self.assistant_id = "asst_pkhPiEMEmYXXb65mRqIkzP6t"
		self.client = OpenAI(
      		api_key=os.environ.get("OPENAI_API_KEY")
        )

	def reflect(self, memories):
		pass
