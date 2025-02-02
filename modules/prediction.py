"""
This module contains class for working on prediction - is it worth trying to take this 
challenge or not.
"""

from xgboost import XGBClassifier
from modules.data_simulation import InitialData


class ModelWork:
    """Class contains functions to take cards name, get their propreties, get this row
    ready for model, load the model and predict the outcome(advice)"""

    def __init__(self):
        self.data = InitialData()
        self.model = XGBClassifier()
        self.model.load_model("xgboost_model.json")

    def get_data_from_tables(self, first, second, third, challenge):
        f_c = self.data.return_row("first", first)
        s_c = self.data.return_row("second", second)
        t_c = self.data.return_row("third", third)
        chal = self.data.return_row("challenge", challenge)

        return (f_c, s_c, t_c, chal)

    def get_data_ready(self, data_list):
        f_c, s_c, t_c, chal = self.get_data_from_tables(
            data_list[0], data_list[1], data_list[2], data_list[4]
        )

        df = f_c.merge(s_c, how="cross")
        df = df.merge(t_c, how="cross")
        df = df.merge(chal, how="cross")
        df["Опыт"] = int(data_list[3])
        drops = ["Испытание", "Происхождение", "Стремление", "Судьба"]
        df = df.drop(drops, axis=1)

        return df

    def predict_target(self, data_list):
        ready_data = self.get_data_ready(data_list)

        return self.model.predict(ready_data[self.model.feature_names_in_])


if __name__ == "__main__":
    model = ModelWork()
    answer = model.predict_target(
        [
            "Фермер",
            "Ученик мастера",
            "Коварный злодей",
            1,
            "Отправиться на поиски еды",
        ]
    )
    print(answer)
    answer = model.predict_target(
        [
            "Охотник",
            "Сорвиголова",
            "Карающая длань",
            1,
            "Украсть, чтобы выжить",
        ]
    )
    print(answer)
