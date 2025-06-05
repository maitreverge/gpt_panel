from App import App


def main():

    app = App()

    print(app.gpt_engine)  # This the API key

    app.mainloop()

    # Prints total spent within the execution
    # ! .total_spent is the getter, ._total_spent is the actual variable
    print(app.gpt_engine.price_engine.total_spent)


main()
