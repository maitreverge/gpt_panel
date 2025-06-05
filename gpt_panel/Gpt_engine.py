from openai import OpenAI
from Price_engine import Price_engine
import tiktoken

MILLION = 1000000


class Gpt_engine():
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

        self.total_token_input = 0
        self.total_token_output = 0
        self.total_token_cache = 0

        self._total_spent = 0

        self.current_answer = ""

        # Those values are for gpt-4.1-nano model, price per token
        self.input_token_price = 0.1 / MILLION
        self.output_token_price = 0.4 / MILLION
        self.cached_token_price = 0.025 / MILLION

        self.token_encoding = tiktoken.encoding_for_model("gpt-4")

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

    def update_tokens(self, input, output, cache):
        """
        Update input, output and cache-tokens, and increment the total spent in OpenAPI usage.
        """
        self.total_token_input += len(self.token_encoding.encode(input))
        self.total_token_output += len(self.token_encoding.encode(output))
        self.total_token_cache += len(self.token_encoding.encode(cache))

        self._total_spent += (
            self.total_token_input * self.input_token_price
            + self.total_token_output * self.output_token_price
            + self.total_token_cache * self.cached_token_price
        )

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

        print(f"CURRENT RESPONSE ID = {self.current_reponse_id}")

        self.update_tokens(prompt, response.output_text, response.output_text)

        # print(response.output_text)

        self.current_answer = response.output_text
    
    # @proprety == Getter
    @property
    def total_spent(self):
        return f"Total spent : ${self._total_spent:.8f}"
