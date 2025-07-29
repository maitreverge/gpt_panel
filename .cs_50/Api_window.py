import customtkinter as ctk
import tkinter as tk
import sys
from openai import OpenAI

WINDOWS_HEIGHT = 800
WINDOWS_WIDTH = 800

LITTLE_WINDOWS_HEIGHT = 400
LITTLE_WINDOWS_WIDTH = 300


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, txt_input="", **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{LITTLE_WINDOWS_HEIGHT}x{LITTLE_WINDOWS_WIDTH}")
        self.title("⛔  INVALID KEY  ⛔")

        self.label = ctk.CTkLabel(
            self,
            text=txt_input,
            font=("Arial", 15),
        )

        self.label.grid(
            row=0,
            column=0,
            padx=LITTLE_WINDOWS_WIDTH * 0.2,
            pady=LITTLE_WINDOWS_HEIGHT * 0.2,
        )


class Api_window(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")

        self.title("API WINDOW PROMPT")
        self.geometry(f"{WINDOWS_HEIGHT}x{WINDOWS_WIDTH}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.toplevel_window = None
        self.env_path = "./.env"
        self.api_key = ""

        self.welcome_text = """
        ** WELCOME TO GPT PANEL **\n
        To get started, please enter your OpenAI API key.\nThis allows the app to connect securely and provide you with powerful AI features.
        """

        self.main_text = ctk.CTkLabel(
            self,
            text=self.welcome_text,
            width=300,
            justify="center",
            font=("Arial", 20),
            wraplength=int(WINDOWS_WIDTH * 0.8),
        )

        self.main_text.grid(row=0, column=0, sticky="we")

        self.api_prompt = tk.Entry(
            self,
            textvariable="testhehe",
            show="\u2022"
        )

        self.api_prompt.grid(row=1, column=0, columnspan=2, padx=(20, 20), sticky="we")

        self.hide_checkbox = ctk.CTkCheckBox(
            self,
            text="DISPLAY API KEY",
            command=self.hide_key,
            width=50,
            height=50,
        )
        self.hide_checkbox.grid(row=1, column=0, pady=(100, 0))

        self.validate_button = ctk.CTkButton(
            self,
            text="VALIDATE",
            command=self.validate_key,
            width=60,
            height=60,
        )
        self.validate_button.grid(row=3, column=0, pady=(0, 100), padx=(75, 0), sticky="w")

        self.cancel_button = ctk.CTkButton(
            self,
            text="CANCEL",
            command=self.quit_program,
            width=60,
            height=60,
        )
        self.cancel_button.grid(row=3, column=0, sticky="e", pady=(0, 100), padx=(0, 75))

    def quit_program(self, event=None):
        """
        Quit the program if the user clicks on the CANCEL button.
        """
        print(f"QUIT THE PROGRAM")
        sys.exit(1)

    def hide_key(self, event=None):
        """
        Selector to switch between "*" and real API key.
        """
        is_checked = self.hide_checkbox.get()

        if is_checked:
            self.api_prompt.configure(show="")
        else:
            self.api_prompt.configure(show="\u2022")

    def validate_key(self, event=None):
        """
        Returns True if the API key is valid, False is not
        """
        self.api_key = self.api_prompt.get().strip()
        client = OpenAI(api_key=self.api_key)
        try:
            client.models.list()
        except Exception as e:
            # !   Warn the user about his invalid key
            print(f"⛔ INCORRECT API KEY")
            self.toplevel_window = ToplevelWindow(
                self, txt_input="INVALID KEY\nPLEASE ENTER A VALID KEY"
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
        # ! quit the intermediate window and switch to the main one.
        self.destroy()