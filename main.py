import tkinter as tk
from tkinter import StringVar, messagebox, IntVar
from widgets.Colors import Colors
from request import get_data


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Weather app")
        self.iconbitmap("images/icon.ico")
        self.config(bg="#14181B")

        # Grid config
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.city_entry_var = StringVar()
        self.scale_var = IntVar()

        self.create_components()

    def create_components(self):
        # Menu
        self.menu = tk.Menu(self, tearoff=False)
        self.submenu = tk.Menu(self)
        self.config_menu = tk.Menu(self)

        self.config_menu.add_radiobutton(label="Celsius", variable=self.scale_var, value=0)
        self.config_menu.add_radiobutton(label="Kelvin", variable=self.scale_var, value=1)
        self.config_menu.add_radiobutton(label="Fahrenheit", variable=self.scale_var, value=2)

        self.menu.add_cascade(label="Config", menu=self.submenu)
        self.submenu.add_cascade(label="Select temperature measurement scales", menu=self.config_menu)

        self.config(menu=self.menu)


        # Search bar
        self.search_bar_frame = tk.Frame(self, bg=Colors.BACKGROUND_BLUE_SEARCH_BAR, highlightbackground=Colors.STRONG_GREY, highlightthickness=1)
        self.search_bar_frame.pack(padx=10, pady=10, fill="both")

        city_entry = tk.Entry(self.search_bar_frame, textvariable=self.city_entry_var, width=15, font=("Bold", 18), bg=Colors.LIGHT_GREY, border=0)
        city_entry.grid(row=0, column=0, padx=5, pady=5)

        city_button = tk.Button(self.search_bar_frame, text="Search", command=self.search)
        city_button.grid(row=0, column=1, padx=5, pady=5)

        city_lbl = tk.Label(self.search_bar_frame, text="Enter a city to display the weather", bg=Colors.BACKGROUND_BLUE_SEARCH_BAR, font=("Arial", 12), fg=Colors.FONT_BLUE)
        city_lbl.grid(row=0, column=2, padx=5, pady=5)

        # Information display
        self.time_lbl = tk.Label(self, text="", font=("Bold", 20), bg=Colors.BACKGROUND_BLUE, fg=Colors.FONT_BLUE)
        self.time_lbl.pack()

        self.location_lbl = tk.Label(self, text="", font=("Bold", 20), bg=Colors.BACKGROUND_BLUE, fg=Colors.FONT_BLUE)
        self.location_lbl.pack()

        self.image = tk.PhotoImage(file="")
        self.image_lbl = tk.Label(self, image=self.image, bg=Colors.BACKGROUND_BLUE, fg=Colors.FONT_BLUE)
        self.image_lbl.pack()

        self.temp_lbl = tk.Label(self, text="", bg=Colors.BACKGROUND_BLUE, fg=Colors.FONT_BLUE)
        self.temp_lbl.pack()

        self.min_temp_lbl = tk.Label(self, text="", bg=Colors.BACKGROUND_BLUE, fg=Colors.FONT_BLUE)
        self.min_temp_lbl.pack()

        self.max_temp_lbl = tk.Label(self, text="", bg=Colors.BACKGROUND_BLUE, fg=Colors.FONT_BLUE)
        self.max_temp_lbl.pack()

        self.weather_lbl = tk.Label(self, text="", bg=Colors.BACKGROUND_BLUE, fg=Colors.FONT_BLUE)
        self.weather_lbl.pack()


    def search(self):
        city = self.city_entry_var.get()
        weather = get_data(city)
        if weather:
            self.time_lbl["text"] = f"{weather[5].strftime('%A, %m/%d/%y')}"
            self.location_lbl["text"] = f"{weather[0]}, {weather[1]}"
            self.image["file"] = f"images/{weather[3]}.png"

            if self.scale_var.get() == 0:
                self.temp_lbl["text"] = f"Temperature: {(weather[2]-273.15):.2f}°C"
                self.min_temp_lbl["text"] = f"Min temperature: {(weather[6] - 273.15):.2f}°C"
                self.max_temp_lbl["text"] = f"Max temperature: {(weather[7] - 273.15):.2f}°C"
            elif self.scale_var.get() == 1:
                self.temp_lbl["text"] = f"Temperature: {weather[2]:.2f}°K"
                self.min_temp_lbl["text"] = f"Min temperature: {weather[6]:.2f}°K"
                self.max_temp_lbl["text"] = f"Max temperature: {weather[7]:.2f}°K"
            else:
                self.temp_lbl["text"] = f"Temperature: {((weather[2]-273.15)*(9/5)+32):.2f}°F"
                self.min_temp_lbl["text"] = f"Min temperature: {((weather[6]-273.15)*(9/5)+32):.2f}°F"
                self.max_temp_lbl["text"] = f"Max temperature: {((weather[7]-273.15)*(9/5)+32):.2f}°F"

            self.weather_lbl["text"] = f"Weather: {weather[4]}"

        else:
            messagebox.showerror("Error", f"Cannot find city {city}")

if __name__ == "__main__":
    window = WeatherApp()
    window.mainloop()
