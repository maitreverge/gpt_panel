import buttons

from App import App
from Gpt_engine import Gpt_engine

def main():

    gpt_engine = Gpt_engine()

    print(gpt_engine)
    
    app = App()

    app.mainloop()

main()
