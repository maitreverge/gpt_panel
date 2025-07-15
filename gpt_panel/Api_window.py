import customtkinter as ctk
import tkinter as tk
import sys
from openai import OpenAI

WINDOWS_HEIGHT = 800
WINDOWS_WIDTH = 800

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, txt_input="", **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text=txt_input)
        self.label.pack(padx=20, pady=20)
        self.title("⛔  INVALID KEY  ⛔")

class Api_window(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")

        self.title("API WINDOW PROMPT")
        self.geometry(f"{WINDOWS_HEIGHT}x{WINDOWS_WIDTH}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.toplevel_window = None

        self.env_path = "../.env"

        ################# ? USEFULL ??
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

        self.hide_checkbox = ctk.CTkCheckBox(
            self,
            text="DISPLAY API KEY",
            command=self.hide_key,
            onvalue="on",
            offvalue="off",
        )

        self.hide_checkbox.grid(row=2, column=0)

        self.validate_button = ctk.CTkButton(
            self,
            text="VALIDATE",
            command=self.validate_key,
        )

        self.validate_button.grid(row=3, column=0)
        self.cancel_button = ctk.CTkButton(
            self,
            text="CANCEL",
            command=self.quit_program,
        )
        self.cancel_button.grid(row=3, column=1)
    
    def quit_program(self, event=None):
        print(f"QUIT THE PROGRAM")
        sys.exit(1)
    
    def hide_key(self, event=None):
        """
        Selector to switch between "*" and real API key.
        """
        raise NotImplementedError

    def validate_key(self, event=None):
        """
        Returns True if the API key is valid, False is not
        """
        self.api_key = self.api_prompt.get(1.0, tk.END).strip()
        client = OpenAI(api_key=self.api_key)
        try:
            client.models.list()
        except Exception as e:
            # !   Warn the user about his invalid key
            print(f"⛔ INCORRECT API KEY")
            self.toplevel_window = ToplevelWindow(
                self,
                txt_input="INVALID KEY, PLEASE ENTER A VALID KEY"
            )
        else:
            # !  Write the key in the format OPEN_AI_KEY=... in the .env file
            self.write_key_env()
    
    def write_key_env(self):
        """
        Write the API key at the root of the repo in the following format:
        OPEN_AI_KEY=...
        """
        with open(self.env_path, "w") as f:
            target = f"OPEN_AI_KEY={self.api_key}"
            f.write(target)
        # raise NotImplementedError