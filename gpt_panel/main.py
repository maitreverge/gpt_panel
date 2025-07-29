from App import App
from Api_validator import Api_validator
from Api_window import Api_window


def intermediate_api_check():
    """
    Opens un a Tkinter Window for the user to prompt his own OpenAI API key.
    The window keeps openning when closed unless `CANCEL` button is pressed.
    """
    while True:
        try:
            starter = Api_validator()
            starter.validate_key()
            break
        except Exception as e:
            # ! Launch the API window
            print(f"LAUNCHING WINDOW API. Error type : {e}")
            api_w = Api_window()
            api_w.mainloop()


def main():

    intermediate_api_check()

    app = App()
    print(app.gpt_engine)
    app.mainloop()
    print(app.gpt_engine.price_engine.total_spent)

main()
