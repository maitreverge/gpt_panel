import customtkinter as ctk
import tkinter as tk
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
            fg_color="#F39C19",
            border_width=3,
            values=self.gpt_engine.models,
            command=self.update_model,
        )

        # Default first model == gpt-4.1-nano
        self.model_selector.set(self.gpt_engine.models[0])

        self.model_selector.grid(
            row=0,
            column=2,
        )

        self.length_slider = ctk.CTkSlider(
            self,
            from_=1,
            to=5,
            # border_color="#EC0808",
            button_color="#FA0808",
            number_of_steps=4,
            command=self.update_length
        )

        self.length_slider.grid(
            row=0,
            column=3,
        )

        self.temperature_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=200,
            # variable=tk.DoubleVar,
            # border_color="#EC0808",
            button_color="#4DFA08",
            number_of_steps=200,
            command=self.update_temperature
        )

        self.temperature_slider.grid(
            row=1,
            column=3,
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
            wrap="word",
        )

        self.prompt_textbox.grid(row=1, column=0, sticky="ew")

        self.prompt_textbox.bind("<KeyRelease>", self.adjust_textbox_height)

        self.prompt_textbox.bind(
            "<KeyRelease-Return>",
            command=self.button_callback
        )

        self.send_button = ctk.CTkButton(
            self,
            text="SEND TO GPT",
            command=self.button_callback,
            image=self.img_send_button,
        )
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

    def update_length(self, event=None):
        self.gpt_engine.lenght_choice = int(self.length_slider.get())
        # print(f"Value of length selector = {int(self.length_slider.get())}")

    def update_temperature(self, event=None):
        """
        Update the temperature in the `gpt_engine` object, dividing it by 100. The CtkSlider only accepts `int` possibles values.
        """
        self.gpt_engine.current_temperature = self.temperature_slider.get() / 100
        print(f"Value of temperature selector = {self.temperature_slider.get() / 100}")

    def update_model(self, event=None):
        print("### UPDATING MODELS ###")
        print(f"Previous models value = {self.gpt_engine.current_model}")
        self.gpt_engine.current_model = self.model_selector.get()
        print(f"Current models value = {self.gpt_engine.current_model}")

    def adjust_textbox_height(self, event=None):
        """
        Dynamically adjust the height of the prompt textbox
        based on total content length
        """
        text = self.prompt_textbox.get("1.0", tk.END)

        num_lines = len(text.split("\n"))
        text_width = self.prompt_textbox.winfo_width()
        avg_chars_per_line = max(1, text_width // 10)

        for line in text.split("\n"):
            if len(line) > avg_chars_per_line:
                num_lines += len(line) // avg_chars_per_line

        # Set height based on content (min 1 line, max 5 lines)
        new_height = min(max(40, num_lines * 20), 120)
        self.prompt_textbox.configure(height=new_height)

    # ! IMPORTANT = write an event=None for callback events with bind
    def button_callback(self, event=None):
        prompt_content = self.prompt_textbox.get(1.0, tk.END).replace("\n", " ")

        print("\n##########\nAPI Response\n##########\n\n")
        self.gpt_engine.send_request(prompt_content)

        self.write_answer(self.gpt_engine.current_answer)

    def write_answer(self, answer):
        """
        Write answer in the answer textbox.
        It unlocks it, write in it,
        then lockit again to avoid the user to modify it
        """
        self.prompt_textbox.delete("1.0", tk.END)

        self.answer_textbox.configure(state="normal")
        self.answer_textbox.insert(index=tk.END, text=answer + "\n")
        self.answer_textbox.configure(state="disable")
