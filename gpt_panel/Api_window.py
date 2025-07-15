import customtkinter as ctk
import tkinter as tk
import sys

WINDOWS_HEIGHT = 800
WINDOWS_WIDTH = 800

class Api_window(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")

        self.title("API WINDOW PROMPT")
        self.geometry(f"{WINDOWS_HEIGHT}x{WINDOWS_WIDTH}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.api_key = ""

        self.welcome_text = """
        GPT PANEL\n
        Welcome! To get started, please enter your OpenAI API key.\nThis allows the app to connect securely and provide you with powerful AI features.
        """

        self.main_text = ctk.CTkLabel(
            self,
            text=self.welcome_text,
            width=300,
            # border_color="#BE3030", # useless need reading doc
            # wrap="word",
            justify="center"
        )

        self.main_text.grid(row=0, column=0, sticky="we")

        # self.main_text.insert(0.0, self.welcome_text)

        self.api_prompt = ctk.CTkTextbox(
            self,
            state="normal"
        )

        self.api_prompt.grid(row=1, column=0, sticky="we")

        self.validate_button = ctk.CTkButton(
            self,
            text="VALIDATE",
            # command=self.quit_program,
        )

        self.validate_button.grid(row=2, column=0)
        self.cancel_button = ctk.CTkButton(
            self,
            text="CANCEL",
            command=self.quit_program,
        )
        self.cancel_button.grid(row=2, column=1)
    
    def quit_program(self, event=None):
        print(f"QUIT THE PROGRAM")
        sys.exit(1)