import flet as ft
import pyautogui
import pandas as pd

class Application(ft.Column):
    
    def __init__(self, page):
        super().__init__() #??????
            
        self.text_style = ft.TextStyle(
            size=16
        )
        self.page = page
        self.column_width = int(self.page.width/3-150)
        self.title_list = ["Происхождение", "Стремление", "Судьба", "Испытание", "Способность"]
        self.variant={}

        self.drops = self.create_choices()
        self.experience = self.set_experience()
        self.check = self.create_check()
        
        self.columns = self.form_columns()
        self.form_page()
        
    def form_page(self):
        
        with open("data/description.txt", "r", encoding="utf-8") as file:
            desc = file.read()
            
        self.page.add(ft.Text(value=desc, size=20, text_align=ft.TextAlign.CENTER))
        self.page.add(
            ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=self.columns[0],
                        col={"sm": 4, "md": 4, "lg": 4},
                        padding=10
                    ),
                    ft.Container(
                        content=self.columns[1],
                        col={"sm": 4, "md": 4, "lg": 4},
                        padding=10
                    ),
                    ft.Container(
                        content=self.columns[2],
                        col={"sm": 4, "md": 4, "lg": 4},
                        padding=10
                    )
                ],
                spacing=10
            )
        )
        self.page.add(
            ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=ft.Text(""),
                        col={"sm": 3, "md": 3, "lg": 3},
                        padding=10
                    ),
                    ft.Container(
                        content=ft.FilledButton(
                            text="Получить подсказку",
                            style=ft.ButtonStyle(
                                text_style=self.text_style
                                )
                            ),
                        col={"sm": 3, "md": 3, "lg": 3},
                        padding=10
                    ),
                    ft.Container(
                        content=ft.Text("Результат предсказания", style=self.text_style),
                        col={"sm": 3, "md": 3, "lg": 3},
                        padding=10
                    ),
                    ft.Container(
                        content=ft.Text(""),
                        col={"sm": 3, "md": 3, "lg": 3},
                        padding=10
                    ),
                ]
            )
        )# on_click
       
    def dropdown_changed(self, e):
        self.variant[dropdown.label] = e
        
    def create_choices(self):
        file_list = [
            "first_card.csv",
            "second_card.csv",
            "third_card.csv",
            "challenge.csv",
            "skill.csv"
        ]
        drop_dict = {}
        for i in range(len(self.title_list)):
            drop_dict[self.title_list[i]] = ft.Dropdown(
                border=ft.InputBorder.NONE,
                enable_filter=True,
                editable=True,
                leading_icon=ft.Icons.SEARCH,
                label=self.title_list[i],
                width=self.column_width,
                options=self.get_options(file_list[i], self.title_list[i]),
                on_change=self.dropdown_changed
            )
        return drop_dict
            
            
    def get_options(self, file, title):
        options = []
        choices = list(pd.read_csv('data/' + file, sep=";")[title])
        for choice in choices:
            options.append(
                    ft.DropdownOption(key=choice)
                )
        return options
    
    def set_experience(self):
        
        exp_text = ft.Text(
            value='Количество очков опыта', 
            size=16,
            text_align=ft.MainAxisAlignment.CENTER
        )
        
        exp_slider = ft.Slider(
            min=0,
            max=3,
            divisions=3,
            value=0,
            label="{value}",
            width=self.column_width,
        )
        
        return (exp_text, exp_slider)
    
    def create_check(self):
        
        check_ability = ft.Checkbox(label="Использовать опыт для \nдопонительной руны способности",
                                    label_style=self.text_style,
                                    value=False)
        check_dark = ft.Checkbox(label="Использовать опыт для \nтемной руны",
                                 label_style=self.text_style,
                                 value=False)

        return (check_ability, check_dark)

    def form_columns(self):
        
        first_col = ft.Column(
                        [self.drops[self.title_list[0]], 
                         self.drops[self.title_list[1]], 
                         self.drops[self.title_list[2]]],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    )
        
        second_col = ft.Column(
                        [ft.Divider(color=ft.Colors.TRANSPARENT),
                         self.experience[0], 
                         self.experience[1], 
                         self.drops[self.title_list[3]]],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    )
        
        third_col =  ft.Column(
                        [self.drops[self.title_list[4]], self.check[0], self.check[1]],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    )
        
        return (first_col, second_col, third_col)

def main(page: ft.Page):
    
    # get screen width and height
    screen_width, screen_height = pyautogui.size()  # width and height of the screen

    # Set the size of our page
    window_width = int(screen_width * 0.5)  
    window_height = int(screen_height * 0.5)  

    # set the dimensions of the screen
    # and where it is placed
    page.window.width = window_width
    page.window.height = window_height
        
    page.title = 'Adventure road challenge helper'
    #page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.padding = 20
    page.update()

    # create application instance
    app = Application(page)

    # add application's root control to the page
    page.add(app)

ft.app(main)