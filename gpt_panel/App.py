import customtkinter as ctk
import tkinter as tk
import buttons
from Gpt_engine import Gpt_engine


WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 950


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")

        self.gpt_engine = Gpt_engine()

        self.title("GPT PANEL")
        self.geometry(f"{WINDOWS_HEIGHT}x{WINDOWS_WIDTH}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.answer_textbox = ctk.CTkTextbox(self, width=200, corner_radius=0, fg_color="red", state="disabled")

        self.answer_textbox.grid(row=0, column=0)

        self.main_prompt = ctk.CTkTextbox(self, width=200, corner_radius=0, padx=10, pady=10)

        self.main_prompt.grid(row=1, column=0, sticky="ew")

        self.button = ctk.CTkButton(self, text="SEND TO GPT NANO", command=self.button_callback)
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

    def button_callback(self):
        prompt_content = self.main_prompt.get('1.0', 'end-1c').strip().replace("\n", " ")
        # print(type(prompt_content))
        # print(f"Content of box = {prompt_content}")

        # Now printing the API response
        # print(f"\n##########\nid_response{self.gpt_engine.current_reponse_id}\n\n##########\n")
        print("\n##########\nAPI Response\n##########\n\n")
        # self.answer_textbox.insert(text="-----", index=tkinter.END)
        self.gpt_engine.send_request(prompt_content)

        # self.answer_textbox.insert(text=self.gpt_engine.current_answer, index=tkinter.END)
        self.write_answer(self.gpt_engine.current_answer)
    
    def write_answer(self, answer):
        """
        Write answer in the answer textbox. It unlocks it, write in it, then lock
        it again to avoid the user to modify it
        """

        self.answer_textbox.configure(state="normal")
        self.answer_textbox.insert(index=tk.END, text=answer + "\n")
        self.answer_textbox.configure(state="disable")