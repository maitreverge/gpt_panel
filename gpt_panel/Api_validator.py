from openai import OpenAI


class Api_validator:
    def __init__(self):
        self.env_file = "../.env"
    
    def validate_key(self):
        """
        This functions checks the validity of an OpenAI API key.
        It raises an error if not valid.
        """
        client = OpenAI(api_key=self.access_key())
        client.models.list()


    def access_key(self):
        """
        Tries to access the OpenAI Key in a file called `.env`

        Returns:
            str: The OpenAI Key.
        """
        with open(self.env_file, "r") as f:
            key = f.readline().split('=')
            assert key[0] == "OPEN_AI_KEY"
            assert key[1]
            return key[1]