'''Provides interface to get prediction from model if it worth to take choosed challenge 
or not. So choose your card name, experience points, challenge and get an advice
'''
import tkinter as tk
from tkinter import ttk
import textwrap
import tkinter.font as font
import pandas as pd
from modules.prediction import ModelWork


class Application:
    '''Class contains fuctions to work with interactive window to choose cards and
    get a prediction'''
    # create window
    def __init__(self):

        with open("data/description.txt", "r", encoding="utf-8") as file:
            self.desc = file.read()

        self.window = tk.Tk()

        w = 700  # width for the Tk root
        h = 450  # height for the Tk root

        # get screen width and height
        ws = self.window.winfo_screenwidth()  # width of the screen
        hs = self.window.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.window.geometry("%dx%d+%d+%d" % (w, h, x, y))

        self.window.title("Adventure road game - challenge")

        self.Font = font.Font(family="Arial", size=12)

        self.description_label = tk.Label(
            self.window,
            text=textwrap.fill(self.desc),
            font=font.Font(family="Arial", size=13),
        )
        self.window.columnconfigure((0), weight=1)
        self.window.rowconfigure((0, 20), weight=1)

        self.description_label.grid(column=0, row=1, rowspan=1, sticky="s")
        # self.window.rowconfigure((1,2), weight=3)
        self.choice_form("first")

    def choice_form(self, time="any"):
        if time != "first":
            self.clear_window()
            self.window.columnconfigure((0), weight=1)
            self.window.rowconfigure((0, 20), weight=1)

        self.create_choices()

        self.btn = tk.Button(
            text="Получить предсказание",
            command=lambda: self.start(),
            font=self.Font,
            height=5,
            width=40,
            wraplength=240,
            justify="center",
        )
        self.btn.grid(column=0, row=20)

    def create_choices(self):
        file_list = [
            "first_card.csv",
            "second_card.csv",
            "third_card.csv",
            "exp.csv",
            "challenge.csv",
            "skill.csv"
        ]
        title_list = ["Происхождение", "Стремление", "Судьба", "Опыт", "Испытание", "Способность"]
        self.var_list = []
        for i in range(len(title_list)):
            self.make_comboboxes(file_list, i, title_list)

    def make_comboboxes(self, file_list, i, title_list):
        self.choices = list(pd.read_csv('data/' + file_list[i], sep=";")[title_list[i]])

        self.var_list.append(tk.StringVar())

        self.label = ttk.Label(self.window, text=title_list[i])
        self.label.grid(column=0, row=2 * (i + 2), sticky="s")
        self.dropdown = ttk.Combobox(
            self.window,
            textvariable=self.var_list[i],
            values=self.choices,
            width=40,
            state="readonly",
        )
        self.dropdown.grid(column=0, row=2 * i + 5, sticky="s")

    def get_model_answer(self):
        model = ModelWork()
        card_list = []
        card_list.extend(v.get() for v in self.var_list)
        answer = model.predict_target(card_list)

        return "Риск стоит того" if answer[0] == 1 else "Это испытание того не стоит"

    def answer_form(self, answer_txt):
        self.clear_window()
        self.description_label = tk.Label(
            self.window,
            text=textwrap.fill(str(answer_txt)),
            font=font.Font(family="Arial", size=13),
        )
        self.window.columnconfigure((0), weight=1)
        self.window.rowconfigure((0, 4), weight=1)

        self.description_label.grid(column=0, row=1, sticky="s")

        self.btn = tk.Button(
            text="Попробовать еще раз",
            command=lambda: self.choice_form("any"),
            font=self.Font,
            height=5,
            width=40,
            wraplength=240,
            justify="center",
        )
        self.btn.grid(column=0, row=3)

    def start(self):
        self.clear_window()
        # self.var.get()
        answer_txt = self.get_model_answer()
        self.answer_form(answer_txt)

    def clear_window(self):
        # Get all widgets in the window
        for widget in self.window.winfo_children():
            widget.destroy()

    def run(self):
        self.window.mainloop()


app = Application()
app.run()
