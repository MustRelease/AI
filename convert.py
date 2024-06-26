from openai import OpenAI
from etc import load_dotenv
import os

class Converter():
	def __init__(self):
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
							"text": "너는 지성이 관찰한 상황 묘사를 연아의 입장으로 다시 작성해야 해\n<예시>\n연아가 나를 바라보며 미소를 지었다.\n<예시답안>나는 지성을 바라보며 미소를 지었다."
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
