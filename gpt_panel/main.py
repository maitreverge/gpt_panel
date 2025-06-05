import buttons

from App import App

def main():

    app = App()

    print(app.gpt_engine) # This the API key

    app.mainloop()

    # Prints total spent within the execution
    print(app.gpt_engine.total_spent)

main()
