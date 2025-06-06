import csv
import tiktoken

MILLION = 1000000


PRICE_FILE = "../assets/price_models.csv"


class Price_engine():
    def __init__(self):
        self.prices = self.price_parser()

        self._total_spent = 0

        self.token_encoding = tiktoken.encoding_for_model("gpt-4")

        # Default pricer
        self.current_price_model = "gpt-4.1-nano"

    # @proprety == Getter
    @property
    def total_spent(self):
        return f"Total spent : ${self._total_spent:.8f}"

    def price_parser(self):
        """
        Extract the prices into a nested dict
        """
        with open(PRICE_FILE, mode="r") as csvfile:
            csvreader = csv.DictReader(csvfile)
            data = [row for row in csvreader]

        nested_dict = {}

        for item in data:
            model_name = item["model"]
            model_data = {
                k: float(v) / MILLION for k, v in item.items() if k != "model"
            }
            nested_dict[model_name] = model_data

        # print(nested_dict)
        return nested_dict

    def update_tokens(self, input, output, cache):
        """
        Update input, output and cache-tokens, and increment the total spent in OpenAPI usage.
        """
        tokens_input = len(self.token_encoding.encode(input))
        tokens_output = len(self.token_encoding.encode(output))
        tokens_cache = len(self.token_encoding.encode(cache))

        # Get prices
        cur_model_prices = self.prices[self.current_price_model]

        self._total_spent += (
            # Input tokens
            tokens_input * cur_model_prices["input"]
            # Output tokens
            + tokens_output * cur_model_prices["output"]
            # Cached tokens
            + tokens_cache * cur_model_prices["cache"]
        )
