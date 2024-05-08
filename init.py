from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

assistant_id = "asst_pkhPiEMEmYXXb65mRqIkzP6t"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)