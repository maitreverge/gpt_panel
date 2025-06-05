from openai import OpenAI
from Price_engine import Price_engine


class Gpt_engine:
    def __init__(self):
        self._api_key = self.read_api_key()
        self.client = OpenAI(api_key=self._api_key)
        self.current_reponse_id = str()
        self.models = [
            "gpt-4.1-nano",
            "gpt-4.1-mini",
            "gpt-4.1",
        ]

        # Move everything related to price in the object Price_engine
        self.price_engine = Price_engine()
        self.current_model = "gpt-4.1-nano"
        self.current_answer = ""

    def __str__(self):
        return f"Current API key= {self._api_key[0:4]}....{self._api_key[-6:-1]}"

    def read_api_key(self):
        """
        Read the API key from the .env file
        """
        result = ""
        with open("../.env", "r") as f:
            result = f.readline().split("=")[1]

        return result

    def send_request(self, prompt):
        args = {
            "model": self.current_model,
            "input": prompt,
        }

        print(f"CURRENT MODEL USED = {self.current_model}")

        # Append the previous context ID
        if self.current_reponse_id:
            args.update({"previous_response_id": self.current_reponse_id})

        response = self.client.responses.create(**args)

        # Save the current conv id.
        self.current_reponse_id = self.current_reponse_id or response.id

        # print(f"CURRENT RESPONSE ID = {self.current_reponse_id}")

        self.price_engine.update_tokens(
            prompt, response.output_text, response.output_text
        )

        # print(response.output_text)

        self.current_answer = response.output_text
