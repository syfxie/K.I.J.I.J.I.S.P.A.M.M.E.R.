import tkinter as tk
from tkinter import *
import customtkinter
import locale

locale.setlocale(locale.LC_ALL, "")


class GUI:
    def __init__(self):
        customtkinter.set_appearance_mode("system")
        self.root = customtkinter.CTk()
        self.root.geometry("400x400")
        self.can_retrieve_input = tk.BooleanVar()

        self.title = customtkinter.CTkLabel(
            master=self.root, text="PriceWhisper", font=("Monaco", 20, "bold")
        )
        self.title.pack(pady=(30, 10))

        self.search_item = customtkinter.CTkEntry(
            master=self.root, placeholder_text="Search Item", font=("Monaco", 11)
        )
        self.search_item.pack(pady=10)

        self.price_range = customtkinter.CTkSlider(
            master=self.root, from_=0, to=3000, command=self._slider_value
        )
        self.price_range.set(0)
        self.price_range.pack(pady=10)

        self.slider_value_label = customtkinter.CTkLabel(
            master=self.root, text="$0", font=("Monaco", 14)
        )
        self.slider_value_label.pack(pady=0)

        self.is_individual_var = tk.IntVar(self.root, 0)
        self.is_individual = customtkinter.CTkRadioButton(
            master=self.root,
            text="Individual",
            font=("Monaco", 12),
            variable=self.is_individual_var,
            value=1,
        )
        self.is_big_search = customtkinter.CTkRadioButton(
            master=self.root,
            text="Big Search",
            font=("Monaco", 12),
            variable=self.is_individual_var,
            value=0,
        )
        self.is_individual.pack(pady=10)
        self.is_big_search.pack(pady=10)

        print("before run button")
        self.run_button = customtkinter.CTkButton(
            master=self.root,
            text="Run",
            font=("Monaco", 14),
            command=self.run_button_clicked,
        )
        self.run_button.pack(pady=20)

        # self.root.mainloop()
        # return self.root

    def _slider_value(self, value):
        formatted_value = locale.currency(int(float(value)), grouping=True)[:-3]
        if value == 3000:
            formatted_value += "+"
        self.slider_value_label.configure(text=formatted_value)

    def run_button_clicked(self):
        self.can_retrieve_input.set(True)
        self.root.quit()  # stops main loop

    def retrieve_input(self):
        dic = {
            "search_item": self.search_item.get(),
            "max_price": self.search_item.get(),
            "is_individual": "true" if self.is_individual_var.get() == 1 else "false",
        }
        return dic
