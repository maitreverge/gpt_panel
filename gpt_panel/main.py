from App import App
from openai import OpenAI
from Api_validator import Api_validator
from Api_window import Api_window
import sys

def main():

    ########### Block for entering the api key
    # while True:
    try:
        starter = Api_validator()
        starter.validate_key()
        # break # ! Encapsulate this later
    except Exception as e:
        # ! Launch the API window
        print(f"LAUNCHING WINDOW API. Error type : {e}")
        api_w = Api_window()
        api_w.mainloop()
            # sys.exit(1)
    
    ########### Block for entering the api key
    
    app = App()

    print(app.gpt_engine)  # This the API key

    app.mainloop()

    # Prints total spent within the execution
    # ! .total_spent is the getter, ._total_spent is the actual variable
    print(app.gpt_engine.price_engine.total_spent)


main()
