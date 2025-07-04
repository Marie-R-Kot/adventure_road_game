"""
This module contains class for working on prediction - is it worth trying to take this 
challenge or not.
"""

from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from modules.data_simulation import InitialData

# from data_simulation import InitialData


class ModelWork:
    """Class contains functions to take cards name, get their propreties, get this row
    ready for model, load the model and predict the outcome(advice)"""

    def __init__(self):
        self.data = InitialData()
        # self.model = CatBoostClassifier()
        # self.model.load_model("catboost_model.bin")
        self.model = XGBClassifier()
        self.model.load_model("xgboost_model.json")

    def get_data_from_tables(self, first, second, third, challenge, skill):
        f_c = self.data.return_row("first", first)
        s_c = self.data.return_row("second", second)
        t_c = self.data.return_row("third", third)
        chal = self.data.return_row("challenge", challenge)
        sk = self.data.return_row("skill", skill)

        return (f_c, s_c, t_c, chal, sk)

    def get_data_ready(self, data_list):
        # Old version of interface
        # f_c, s_c, t_c, chal, sk = self.get_data_from_tables(
        #     data_list[0], data_list[1], data_list[2], data_list[4], data_list[5]
        # )

        cards_name, exp, skill_check, dark_check = data_list
        f_c, s_c, t_c, chal, sk = self.get_data_from_tables(
            cards_name[0], cards_name[1], cards_name[2], cards_name[3], cards_name[4]
        )
        
        df = f_c.merge(s_c, how="cross")
        df = df.merge(t_c, how="cross")
        df = df.merge(chal, how="cross")
        df = df.merge(sk, how="cross")
        df["Опыт"] = exp
        drops = [
            "Испытание",
            "Происхождение",
            "Стремление",
            "Судьба",
        ]  # , "Способность"]
        df = df.drop(drops, axis=1)

        return df

    def predict_target(self, data_list):
        ready_data = self.get_data_ready(data_list)
        return self.model.predict(ready_data[self.model.feature_names_in_])  # _in_])


if __name__ == "__main__":
    model = ModelWork()
    answer = model.predict_target(
        [
            "Фермер",
            "Ученик мастера",
            "Коварный злодей",
            1,
            "Отправиться на поиски еды",
            "Ловкость",
        ]
    )
    print(answer)
    answer = model.predict_target(
        ["Охотник", "Сорвиголова", "Карающая длань", 1, "Украсть, чтобы выжить", "Сила"]
    )
    print(answer)
