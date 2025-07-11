"""
Module provides classes to create player's turn and dataset with its combination
One player created by combining his three card, additional skill(if exists)
and his experience points. We have 19552 possible combination
One turn created by combining one player with some challenge from challenges list(31 in total)
"""

import os
import pandas as pd
from math import comb
from dataclasses import dataclass
import random
from typing import Dict

data_dir = os.path.join(os.getcwd(), "data")


@dataclass
class Player:
    """Class contains function to create one player and return his id"""

    first_card: pd.Series
    second_card: pd.Series
    third_card: pd.Series
    experience: int
    skill: str

    def define_player(self, player_id: int) -> Dict:
        """Define a player dictionary based on card attributes."""
        return {
            "Игрок": player_id,
            "Происхождение": self.first_card.Происхождение,  
            "Руна_1": self.first_card.Руна_1,  
            "Руна_2": self.first_card.Руна_2,  
            "Стремление": self.second_card.Стремление, 
            "Опция": self.second_card.Опция,  
            "Судьба": self.third_card.Судьба,  
            "Цель_1": self.third_card.Цель_1,  
            "Цель_2": self.third_card.Цель_2,  
            "Цель_3": self.third_card.Цель_3,  
            "Опыт": self.experience,
            "Способность": self.skill,
        }

    def return_player(self, player_id: int) -> Dict:
        """Return the player dictionary."""
        return self.define_player(player_id)


@dataclass
class Turn:
    """Class contains function to create one turn - combine player, challenge and simulate 
    the result of this turn
    - which is actually advice is it worth to take this challenge or not"""

    player: Dict
    challenge: Dict
    extra_check: bool
    dark_check: bool

    def count_rune_probability(
        self, main: int, extra: int, dark: int, threshold: int
    ) -> float:
        """Calculate the probability of meeting the rune threshold."""
        n1 = 3  # Runes that can be 0 or 1
        n2 = main + extra + dark  # Runes that can be 1 or 2

        # Calculate probabilities for the first group of runes (0 or 1)
        prob1 = {k1: comb(n1, k1) * (0.5**n1) for k1 in range(n1 + 1)}

        # Calculate probabilities for the second group of runes (1 or 2)
        prob2 = {k2: comb(n2, k2) * (0.5**n2) for k2 in range(n2 + 1)}

        return sum(
            prob1[sum1] * prob2[sum2]
            for sum1 in prob1
            for sum2 in prob2
            if (sum1 + sum2) >= threshold
        )

    def simulate_turn(self) -> int:
        """Simulate whether the player should attempt the challenge."""
        main_rune = sum(
            1
            for rune in [
                self.player["Руна_1"],
                self.player["Руна_2"],
                self.player["Способность"],
            ]
            if rune
            in [self.challenge["Основная руна"], self.challenge["Дополнительная руна"]]
        )

        dark_rune = int(self.player["Опыт"] > 0 and self.dark_check is True)

        extra_rune = int(
            self.player["Опыт"] > 0
            and self.player["Опция"]
            in [self.challenge["Основная руна"], self.challenge["Дополнительная руна"]]
            and self.extra_check is True
        )

        rune_prob = self.count_rune_probability(
            main_rune, extra_rune, dark_rune, self.challenge["Сложность"]
        )

        if 0.3 <= rune_prob < 0.5 and self.challenge["Основная руна"] in [
            self.player["Цель_1"],
            self.player["Цель_2"],
            self.player["Цель_3"],
        ]:
            return 1
        elif rune_prob >= 0.5:
            return 1
        else:
            return 0

    def return_turn(self, if_target: bool) -> pd.DataFrame:
        """Return a DataFrame representing the turn."""
        if if_target:
            self.challenge["Стоит ли пробовать"] = self.simulate_turn()

        df = pd.DataFrame([self.player]).merge(pd.DataFrame([self.extra_check], columns=["Исп. доп. руны"]), how="cross")
        df = df.merge(pd.DataFrame([self.dark_check], columns=["Исп. руны тьмы"]), how="cross")
        df = df.merge(pd.DataFrame([self.challenge]), how="cross")
        
        return df
        # return pd.DataFrame([self.player]).merge(
        #     pd.DataFrame([self.challenge]), how="cross"
        # )


class InitialData:
    """Class contains functions to create turns DataFrame of given length, to define all
    possible player combination and to return one propreties of exact card"""

    def __init__(self):
        self.first_cards = pd.read_csv("data/first_card.csv", sep=";")
        self.second_cards = pd.read_csv("data/second_card.csv", sep=";")
        self.third_cards = pd.read_csv("data/third_card.csv", sep=";")
        self.challenges = pd.read_csv("data/challenge.csv", sep=";")
        self.skills = pd.read_csv("data/skill.csv", sep=";")
        self.players = self.define_all_players()

    def _runes_check(self, exp, extra, dark):
        if exp > 1:
            return (extra, dark)
        elif exp == 0:
            return (False, False)
        else:
            if False in [extra, dark]:
                return (extra, dark)
            else:
                return random.choice([(False, True), (True, False)])
    
    def define_all_players(self) -> pd.DataFrame:
        players_list = []
        player_id = 1
        for first_card in self.first_cards.itertuples(index=False):
            for second_card in self.second_cards.itertuples(index=False):
                for third_card in self.third_cards.itertuples(index=False):
                    cards = [
                        first_card.Руна_1,
                        first_card.Руна_2,
                        second_card.Опция,
                        third_card.Цель_1,
                        third_card.Цель_2,
                        third_card.Цель_3,
                    ]
                    if "Нет" not in cards:
                        cards.append("Нет")

                    for experience in range(4):
                        for card in set(cards):
                            player = Player(
                                first_card, second_card, third_card, experience, card
                            )
                            players_list.append(player.return_player(player_id))
                            player_id += 1
        # Convert the list of dictionaries into a DataFrame
        return pd.DataFrame(players_list)

    def define_turns(self, count: int, if_target: bool) -> pd.DataFrame:
        """Generate a specified number of turns."""
        turns_list = []

        for _ in range(count):
            player = self.players.sample(1).iloc[0].to_dict()
            challenge = self.challenges.sample(1).iloc[0].to_dict()
            extra_check = random.choice([True, False])
            dark_check = random.choice([True, False])
            extra_check, dark_check = self._runes_check(player["Опыт"], extra_check, dark_check)
            turn = Turn(player, challenge, extra_check, dark_check)
            turns_list.append(turn.return_turn(if_target))

        return pd.concat(turns_list, ignore_index=True)

    def return_row(self, card_type: str, row_name: str) -> pd.DataFrame:
        """Return a specific row from the card data."""
        card_map = {
            "first": ("Происхождение", self.first_cards),
            "second": ("Стремление", self.second_cards),
            "third": ("Судьба", self.third_cards),
            "challenge": ("Испытание", self.challenges),
            "skill": ("Способность", self.skills),
        }
        features_cat = [
            "Руна_1",
            "Руна_2",
            "Опция",
            "Цель_1",
            "Цель_2",
            "Цель_3",
            "Основная руна",
            "Дополнительная руна",
            "Способность",
        ]

        col_name, cards = card_map[card_type]
        if card_type == "challenge":
            dummies = cards[[col_name, "Сложность"]]
        elif card_type == "skill":
            dummies_d = pd.get_dummies(
                cards, prefix=col_name, drop_first=True, dtype=int
            )
            dummies = pd.concat([cards, dummies_d], axis=1)
            return dummies[dummies[col_name] == row_name]
        else:
            dummies = cards[[col_name]]

        for feature in features_cat:
            if feature in cards.columns:
                dummies_d = pd.get_dummies(
                    cards[feature], prefix=feature, drop_first=True, dtype=int
                )
                dummies = pd.concat([dummies, dummies_d], axis=1)

        return dummies[dummies[col_name] == row_name]
