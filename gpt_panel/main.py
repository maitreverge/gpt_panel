from App import App
from openai import OpenAI
from Api_validator import Api_validator
import sys

def main():

    ########### Block for entering the api key
    try:
        starter = Api_validator()
        starter.validate_key()
    except Exception as e:
        # ! Launch the API window
        print(f"LAUNCHING WINDOW API. Error type : {e}")
        sys.exit(1)
    
    ########### Block for entering the api key
    
    app = App()

    print(app.gpt_engine)  # This the API key

    app.mainloop()

    # Prints total spent within the execution
    # ! .total_spent is the getter, ._total_spent is the actual variable
    print(app.gpt_engine.price_engine.total_spent)


main()
