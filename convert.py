from openai import OpenAI
from etc import load_dotenv
import os

class Converter():
	def __init__(self):
		load_dotenv(override=True)
		self.assistant_id = "asst_pkhPiEMEmYXXb65mRqIkzP6t"
		self.client = OpenAI(
			api_key=load_dotenv(".env")
		)

	def convert_description(self, sentence):
		completion = self.client.chat.completions.create(
			model="gpt-4o",
			messages=[
				{
					"role": "system",
					"content": [
						{
							"type": "text",
							"text": "너는 지성이 관찰한 상황 묘사를 연아의 입장으로 다시 작성해야 해"
						}
					]
				},
				{
					"role": "user",
					"content": [
						{
							"type": "text",
							"text": sentence
						}
					]
				}
			],
			temperature=0.0,
			max_tokens=256,
			top_p=1.0,
			frequency_penalty=0,
			presence_penalty=0
		)
		print(completion.choices[0].message.content)
		return completion.choices[0].message.content
