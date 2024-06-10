from openai import OpenAI
from dotenv import load_dotenv
import os
from controller import Controller
import ast
import re

controller = Controller()

class Reflecter:
	def __init__(self):
		load_dotenv(override=True)
		self.assistant_id = "asst_pkhPiEMEmYXXb65mRqIkzP6t"
		self.client = OpenAI(
      		api_key=os.environ.get("OPENAI_API_KEY")
        )


	def get_importance(self, userId):
		input = "<예시>\n"
		input += \
"""Statements about 나와 지성
0. 나는 '이것 좀 봐, 내가 폐허에 있던 무기를 주워 왔어!'라고 말했다.
1. 나는 '총, 수류탄, 칼이 있는데 어떤 걸 쓸래?'라고 말했다.
2. 지성은 '나는 주로 총을 써. 다른 건 별로 안 쓰지.'라고 말했다.
3. 나는 아, 좋아! 총을 잘 쓴다니 다행이네!라고 말했다
명령 : 위 문장을 차례대로 1-10 범위로 점수를 매긴 리스트만 출력한다. (예시 : [5, 8, 2]) 1점은 문맥에서 중요하지 않은 말(지성의 정보가 잘 드러나지 않는 문장)이고, 10점은 문맥에서 중요한 말(지성의 정보가 잘 드러난 문장)이야.
<예시 답>
[3, 6, 10, 7]\n
"""
		input += "Statements about 나(연아)와 지성\n"
		buffer_memory = controller.load_buffer(userId)
		for i, data in enumerate(buffer_memory):
			input = input + str(i) + ". " + data["observation"] + "\n"
		input += "명령 : 위 문장을 차례대로 1-10 범위로 점수를 매긴 리스트만 출력한다. (예시 : [5, 8, 2]) 1점은 문맥에서 중요하지 않은 말(지성의 정보가 잘 드러나지 않는 문장)이고, 10점은 문맥에서 중요한 말(지성의 정보가 잘 드러난 문장)이다."
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
		importance_list = ast.literal_eval(completion.choices[0].message.content)
		for data, score in zip(buffer_memory, importance_list):
			data["importance"] = round(0.1 * score, 1)
		return buffer_memory

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

	def reflect_anynum(self, userId):
		input = "<예시>\n"
		input += \
"""
Statements about 나와 지성\n
0. 나는 '이것 좀 봐, 내가 폐허에 있던 무기를 주워 왔어!'라고 말했다.
1. 나는 '총, 수류탄, 칼이 있는데 어떤 걸 쓸래?'라고 말했다.
2. 지성은 '나는 주로 총을 써. 다른 건 별로 안 쓰지.'라고 말했다.
3. 나는 아, 좋아! 총을 잘 쓴다니 다행이네!라고 말했다.
What high-level insights can you infer from the above statements about 지성 in Korean? (example format: insight (because of [1, 5, 3]))

<예시 답>
1. 지성은 무기를 사용할 줄 안다. (because of [2, 3])
2. 지성은 총기를 선호한다. (because of [2])
3. 지성은 전투 상황에 익숙하다. (because of [0, 1, 2])

"""
		input += "Statements about 나와 지성\n"
		response = controller.load_buffer(userId)
		for i, data in enumerate(response):
			input = input + str(i) + ". " + data["observation"] + "\n"
		input += "What high-level insights can you infer from the above statements about 지성 in Korean? (example format: insight (because of [1, 5, 3]))"
		print(input)
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
		result = completion.choices[0].message.content
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
		    },
			{
      		  "role": "assistant",
      		  "content": [
      		    {
      		      "type": "text",
      		      "text": result
      		    }
      		  ]
   			},
			{
		      "role": "user",
		      "content": [
		        {
		          "type": "text",
		          "text": "출력 형식은 그대로 유지하고, 중복된 insight 혹은 맞지 않은 것은 제거하여 insight만 출력해줘"
		        }
		      ]
		    },
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
				l = re.findall(r'\[(.*?)\]', s)
				l = [int(num) for num in l[0].split(', ')]
				controller.save(userId, "00:00:00", s.split(".")[1].split("(")[0], 1.0, reason_list=l)
		except:
			print("Reflect Format Error : Try again")
			return 500
		return 200

