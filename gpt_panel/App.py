import customtkinter
import buttons
from Gpt_engine import Gpt_engine


WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 950

class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.values = values
        self.checkboxes = []
        self.title = title

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="red", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.gpt_engine = Gpt_engine()

        self.title("GPT PANEL")
        self.geometry(f"{WINDOWS_HEIGHT}x{WINDOWS_WIDTH}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_prompt = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)

        self.main_prompt.grid(row=0, column=0, sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="SEND TO GPT NANO", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        prompt_content = self.main_prompt.get('1.0', 'end-1c').strip().replace("\n", " ")
        # print(type(prompt_content))
        # print(f"Content of box = {prompt_content}")

        # Now printing the API response
        print("\n##########\nAPI Response\n##########\n\n")
        self.gpt_engine.send_request(prompt_content)



