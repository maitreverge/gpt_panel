import customtkinter as ctk
import tkinter as tk
import buttons
from PIL import Image
from Gpt_engine import Gpt_engine


WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 950


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.img_send_button = ctk.CTkImage(
            dark_image=Image.open("../assets/dark_send.jpg")
        )

        ctk.set_appearance_mode("light")

        self.gpt_engine = Gpt_engine()

        self.title("GPT PANEL")
        self.geometry(f"{WINDOWS_HEIGHT}x{WINDOWS_WIDTH}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        
        self.model_selector = ctk.CTkSegmentedButton(
            self,
            values=["Value 1", "Value 2", "Value 3"],
            command=segmented_button_callback
        )

        self.answer_textbox = ctk.CTkTextbox(
            self,
            corner_radius=10,
            fg_color="#C0DF85",
            state="disabled",
            border_width=5,
            border_color="#000000",
        )

        self.answer_textbox.grid(row=0, column=0, sticky="we")

        self.prompt_textbox = ctk.CTkTextbox(
            self,
            corner_radius=10,
            border_width=5,
            border_color="#000000",
            height=40,
            wrap="word"
        )

        self.prompt_textbox.grid(row=1, column=0, sticky="ew")

        self.prompt_textbox.bind("<KeyRelease>", self.adjust_textbox_height)

        # ! IMPLEMENT BUTTON ENTER = SEND PROMPT
        self.prompt_textbox.bind("<KeyRelease-Return>", command=self.button_callback)

        self.send_button = ctk.CTkButton(
            self,
            text="SEND TO GPT",
            command=self.button_callback,
            image=self.img_send_button,
        )
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")
    
    def adjust_textbox_height(self, event=None):
        """Dynamically adjust the height of the prompt textbox based on content"""
        # Get text content
        text = self.prompt_textbox.get("1.0", tk.END)
        
        # Count number of lines (accounting for word wrap)
        num_lines = len(text.split('\n'))
        text_width = self.prompt_textbox.winfo_width()
        avg_chars_per_line = max(1, text_width // 10)  # Approximate chars per line
        
        # Add wrapped lines
        for line in text.split('\n'):
            if len(line) > avg_chars_per_line:
                num_lines += len(line) // avg_chars_per_line
        
        # Set height based on content (min 1 line, max 5 lines)
        new_height = min(max(40, num_lines * 20), 120)
        self.prompt_textbox.configure(height=new_height)

    # ! IMPORTANT = write an event=None for callback eneds with bind
    def button_callback(self, event=None):
        prompt_content = self.prompt_textbox.get(1.0, tk.END).strip().replace("\n", " ")
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
        self.prompt_textbox.delete("1.0", tk.END)

        self.answer_textbox.configure(state="normal")
        self.answer_textbox.insert(index=tk.END, text=answer + "\n")
        self.answer_textbox.configure(state="disable")
