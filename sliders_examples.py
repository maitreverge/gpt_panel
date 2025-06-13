import customtkinter as ctk

class CTkSliderWithValue(ctk.CTkFrame):
    def __init__(self, master, title="Slider", min_value=0, max_value=100, default_value=50, width=300, **kwargs):
        super().__init__(master, **kwargs)
        
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = ctk.DoubleVar(value=default_value)
        
        # Create title label
        self.title_label = ctk.CTkLabel(self, text=title, anchor="w")
        self.title_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))
        
        # Create value label
        self.value_label = ctk.CTkLabel(self, text=str(default_value), width=50)
        self.value_label.grid(row=0, column=1, sticky="e", padx=5, pady=(5, 0))
        
        # Create slider
        self.slider = ctk.CTkSlider(
            self, 
            from_=min_value, 
            to=max_value, 
            variable=self.current_value,
            width=width,
            command=self._update_value_label
        )
        self.slider.grid(row=1, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="ew")
        
        # Initialize value display
        self._update_value_label(default_value)
    
    def _update_value_label(self, value):
        # Update the display with the current value
        formatted_value = int(value) if isinstance(value, int) else value
        self.value_label.configure(text=f"{formatted_value}")
        
    def get(self):
        # Return the current slider value
        return self.current_value.get()
    
    def set(self, value):
        # Set the slider value
        self.current_value.set(value)
        self._update_value_label(value)

import customtkinter as ctk

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("CTk Slider Example")
        self.geometry("400x300")
        
        # Create frame for sliders
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Add sliders with different configurations
        self.brightness_slider = CTkSliderWithValue(
            self.frame, 
            title="Brightness", 
            min_value=0, 
            max_value=100, 
            default_value=50
        )
        self.brightness_slider.pack(pady=10, padx=10, fill="x")
        
        self.volume_slider = CTkSliderWithValue(
            self.frame, 
            title="Volume", 
            min_value=0, 
            max_value=10, 
            default_value=5
        )
        self.volume_slider.pack(pady=10, padx=10, fill="x")
        
        # Add a button to print values
        self.button = ctk.CTkButton(
            self.frame, 
            text="Get Values", 
            command=self.print_values
        )
        self.button.pack(pady=10)
    
    def print_values(self):
        print(f"Brightness: {self.brightness_slider.get()}")
        print(f"Volume: {self.volume_slider.get()}")

if __name__ == "__main__":
    app = App()
    app.mainloop()