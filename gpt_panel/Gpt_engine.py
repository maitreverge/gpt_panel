import openai

class Gpt_engine():
    def __init__(self):
        self._api_key = self.read_api_key()
    
    def __str__(self):
        return f"Current API key= {self._api_key}"
    
    def read_api_key(self):
        result = ""
        with open("../.env", "r") as f: 
            result = f.readline().split("=")[1]
        return result

    

