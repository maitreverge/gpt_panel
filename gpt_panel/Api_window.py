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
        self.grid_rowconfigure(0, weight=1)

        self.cancel_button = ctk.CTkButton(
            self,
            text="CANCEL",
            command=self.quit_program,
        )
        self.cancel_button.grid(row=2, column=0)
    
    def quit_program(self, event=None):
        print(f"QUIT THE PROGRAM")
        sys.exit(1)