from openai import OpenAI

try:
    client = OpenAI(api_key="sjdhbvjshb")
    client.models.list()
except Exception as e:
    print(f"Fail. Error = {e}")