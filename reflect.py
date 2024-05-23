from openai import OpenAI
from dotenv import load_dotenv
import os
from controller import Controller

controller = Controller()

class Reflecter:
	def __init__(self):
		load_dotenv(override=True)
		self.assistant_id = "asst_pkhPiEMEmYXXb65mRqIkzP6t"
		self.client = OpenAI(
      		api_key=os.environ.get("OPENAI_API_KEY")
        )

	def reflect(self, userId):
		input = "Statements about 나와 지성\n"
		response = controller.load_buffer(userId)
		for i, data in enumerate(response):
			input = input + str(i) + ". " + data["observation"] + "\n"
		input += "What 3 high-level insights can you infer from the above statements about 지성 in Korean? (example format: insight (because of 1, 5, 3))"
		completion = self.client.chat.completions.create(
		  model="gpt-4o",
		  messages=[
		    {
		      "role": "user",
		      "content": [
		        {
		          "type": "text",
		          "text": input
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
		try:
			insights = completion.choices[0].message.content.split('\n')
			for s in insights:
				controller.save(userId, "00:00:00", s.split(".")[1].split("(")[0], 1.0)
		except:
			print("Reflect Format Error : Try again")
			return 500
		return 200
