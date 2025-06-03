import buttons

from App import App

def main():

    app = App()

    print(app.gpt_engine) # This the API key

    app.mainloop()

    print(app.gpt_engine.total_spent)

main()
