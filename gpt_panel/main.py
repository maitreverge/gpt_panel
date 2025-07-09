from App import App
from openai import OpenAI

def main():

    ########### Block for entering the api key
    # try:
    #     test_client = OpenAI(api_key="")

    # except Exception as e:
    #     ...
    
    ########### Block for entering the api key
    
    app = App()

    print(app.gpt_engine)  # This the API key

    app.mainloop()

    # Prints total spent within the execution
    # ! .total_spent is the getter, ._total_spent is the actual variable
    print(app.gpt_engine.price_engine.total_spent)


main()
