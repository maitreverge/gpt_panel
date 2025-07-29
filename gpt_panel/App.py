import customtkinter as ctk
import tkinter as tk
from PIL import Image
from Gpt_engine import Gpt_engine
from tktooltip import ToolTip
# https://pypi.org/project/tkinter-tooltip/

"""
padx=(left, right) or padx=value - adds horizontal padding
pady=(top, bottom) or pady=value - adds vertical padding
"""

WINDOWS_WIDTH = 800
WINDOWS_HEIGHT = 1100

MIN_TOKEN_OUTPUT = 16
MAX_TOKEN_OUTPUT = 32768

class CtkToolTip():
    """
    Custom class for creating TooTips specifically for main window sliders.
    """
    def __init__(self, frame, row_nb, hover_msg):

        self.length_info_button = ctk.CTkButton(
            frame, # ! frame = self.frame_sliders from App (tk container for all 3 sliders)
            text="?",               
            width=15,             
            height=15,           
            corner_radius=15,       
            font=("Arial", 14),
            fg_color="#3a3a3a",     
            hover_color="#505050", 
            text_color="white",
        )

        self.length_info_button.grid(
            row=row_nb,
            column=0,
            padx=5,
            pady=5,
        )
        # Hover message
        ToolTip(self.length_info_button, msg=hover_msg)


class CTkSliderWithValue(ctk.CTkFrame):
    def __init__(self, master, title="Slider", min_value=0, max_value=100, default_value=50, width=300, nb_steps=5, passed_function=None, is_temperature=False, **kwargs):
        super().__init__(master, **kwargs)
        
        self.passed_function = passed_function

        self.min_value = min_value
        self.max_value = max_value
        self.current_value = ctk.DoubleVar(value=default_value)
        
        # Create title label
        self.title_label = ctk.CTkLabel(self, text=title, anchor="w")
        self.title_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))
        
        # Create value label
        self.value_label = ctk.CTkLabel(self, text=str(int(default_value)), width=50)
        self.value_label.grid(row=0, column=1, sticky="e", padx=5, pady=(5, 0))
        
        # Create slider
        self.slider = ctk.CTkSlider(
            self, 
            from_=min_value, 
            to=max_value, 
            variable=self.current_value,
            width=width,
            command=lambda value: self._update_value_label(value, is_temperature, call_callback=True),
            number_of_steps=nb_steps,
            # fg_color="#0004FF", # ! This foreground change the color of the slider itself
            button_color="#7AA4FF",
            button_hover_color="#0041F5",
            progress_color="#0087F5",

        )

        self.slider.grid(row=1, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="ew")
        
        """
        The callback is called before self.length_slider exists on your App instance.
        Only call the callback after the widget is fully initialized and attached to the parent.
        Use a flag to control when the callback is called.
        """
        # Initialize value display
        self._update_value_label(default_value, is_temperature, call_callback=False)

    def _update_value_label(self, value, is_temperature, call_callback=True):
        """
        Displays the current value of the slider.
        Format value to 2 digits float number if the slider
        is the temparture slider
        """
        formatted_value = f"{value:.2f}" if is_temperature else int(value)
        
        self.value_label.configure(text=f"{formatted_value}")
        if self.passed_function and call_callback:
            self.passed_function()

    def get(self):
        """
        Get the current slider value
        """
        return self.current_value.get()
    
    def set(self, value):
        """
        Set the slider value
        """
        self.current_value.set(value)
        self._update_value_label(value)


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

        self.window_label_top = ctk.CTkLabel(
            self,
            text="GPT PANEL",
            font=("Nimbus Mono Ps", 45)
        )
        self.window_label_top.grid(row=0, column=0, columnspan=3, sticky="we")

        self.window_label_bottom = ctk.CTkLabel(
            self,
            text="Made with ❤️ by maitreverge",
            font=("Nimbus Mono Ps", 12)
        )
        self.window_label_bottom.grid(row=4, column=1, padx=10, pady=10)

        self.model_selector = ctk.CTkSegmentedButton(
            self,
            fg_color="#89DEFF",
            border_width=3,
            values=self.gpt_engine.models,
            command=self.update_model,
            font=("Bembo", 17),
            text_color_disabled="#817F7B",
        )
        # Default first model == gpt-4.1-nano
        self.model_selector.set(self.gpt_engine.models[0])
        self.model_selector.grid(
            row=1,
            column=2,
        )

        self.frame_sliders = ctk.CTkFrame(self)
        self.frame_sliders.grid(row=2, column=2, pady=(0, 40))

        self.length_info_button = CtkToolTip(
            self.frame_sliders,
            0, # row_nb
            """1 - Concise\n2 - Brief\n3 - Balanced\n4 - Detailed\n5 - Extensive"""
        )

        self.length_slider = CTkSliderWithValue(
            self.frame_sliders,
            title="LENGTH",
            min_value=1, 
            max_value=5, 
            default_value=3,
            nb_steps=4,
            passed_function=self.update_length,
            is_temperature=False,
        )
        self.length_slider.grid(
            row=0,
            column=1,
            padx=10,
            pady=5,
        )

        self.temperature_info_button = CtkToolTip(
            self.frame_sliders,
            1, # row_nb
            "Controls randomness\nLowering temperature turns the models deterministic and repetitive."
        )

        self.temperature_slider = CTkSliderWithValue(
            self.frame_sliders,
            title="TEMPERATURE",
            min_value=0, 
            max_value=2, 
            default_value=1,
            nb_steps=200,
            passed_function=self.update_temperature,
            is_temperature=True,
        )
        self.temperature_slider.grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
        )

        self.max_tokens_info_button = CtkToolTip(
            self.frame_sliders,
            2, # row_nb
            "Controls the total maximum length the answer will be.\n(100 tokens ~= 75 words)"
        )
        self.max_output_tokens_slider = CTkSliderWithValue(
            self.frame_sliders,
            title="MAX TOKEN OUTPUT",
            min_value=MIN_TOKEN_OUTPUT, 
            max_value=MAX_TOKEN_OUTPUT,
            default_value=2048,
            nb_steps=MAX_TOKEN_OUTPUT - MIN_TOKEN_OUTPUT - 1,
            passed_function=self.update_max_output_tokens,
            is_temperature=False,
        )

        self.max_output_tokens_slider.grid(
            row=2,
            column=1,
            padx=10,
            pady=5,
        )

        self.answer_textbox = ctk.CTkTextbox(
            self,
            corner_radius=10,
            fg_color="#1DB6FD",
            state="disabled",
            border_width=5,
            border_color="#000000",
            height=350,
        )
        self.answer_textbox.grid(row=1, column=0, columnspan=2, sticky="we", padx=10, pady=10)

        self.prompt_textbox = ctk.CTkTextbox(
            self,
            corner_radius=10,
            border_width=5,
            border_color="#000000",
            width=60,
            height=60,
            wrap="word",
        )
        self.prompt_textbox.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.prompt_textbox.bind("<KeyRelease>", self.adjust_textbox_height)
        self.prompt_textbox.bind(
            "<KeyRelease-Return>",
            command=self.button_callback
        )

        self.send_button = ctk.CTkButton(
            self,
            text="SEND TO GPT",
            width=60,
            height=60,
            corner_radius=40,
            command=self.button_callback,
            image=self.img_send_button,
        )
        self.send_button.grid(row=3, column=2, padx=42, pady=10, sticky="w")

    def update_length(self, event=None):
        """ Update the length choice in the `gpt_engine` object."""
        self.gpt_engine.lenght_choice = int(self.length_slider.get())

    def update_temperature(self, event=None):
        """
        Update the temperature in the `gpt_engine` object, dividing it by 100. The CtkSlider only accepts `int` possibles values.
        """
        self.gpt_engine.current_temperature = self.temperature_slider.get()
    
    def update_max_output_tokens(self, event=None):
        """
        Slider function which updates the maximum amount of tokens for a given API response.
        """
        self.gpt_engine.max_output_tokens = int(self.max_output_tokens_slider.get())

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

        # Limit the height to a maximum of 100 lines
        # and a minimum of 40 lines
        new_height = min(max(40, num_lines * 20), 100)
        self.prompt_textbox.configure(height=new_height)

    # ! IMPORTANT = write an event=None for callback events with bind
    def button_callback(self, event=None):
        """
        Handle button click event to send prompt content to GPT.
        """
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