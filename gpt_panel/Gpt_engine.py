from openai import OpenAI
import os


class Gpt_engine:
    def __init__(self):
        self._api_key = self.read_api_key()
        self.client = OpenAI(api_key=self._api_key)

    def __str__(self):
        return f"Current API key= {self._api_key[0:4]}....{self._api_key[-4-1]}"

    def read_api_key(self):
        result = ""
        with open("../.env", "r") as f:
            result = f.readline().split("=")[1]
        
        return result

    def send_request(self, prompt):
        response = self.client.responses.create(
            model="gpt-4.1-nano",  # nano is the cheapest so far
            input=prompt
        )
        print(response.output_text)
