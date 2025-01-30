import pandas as pd
from math import comb


class Player:

    def __init__(self, first_card, second_card, third_card, experience) -> None:
        self.first_card = first_card
        self.second_card = second_card
        self.third_card = third_card
        self.experience = experience

    def define_player(self, count):

        self.player = {
            'Игрок': count,
            'Происхождение': self.first_card['Происхождение'],
            'Руна_1': self.first_card['Руна_1'],
            'Руна_2': self.first_card['Руна_2'],
            'Стремление': self.second_card['Стремление'],
            'Опция': self.second_card['Опция'],
            'Судьба': self.third_card['Судьба'],
            'Цель_1': self.third_card['Цель_1'],
            'Цель_2': self.third_card['Цель_2'],
            'Цель_3': self.third_card['Цель_3'],
            'Опыт': self.experience
        }

    def return_player(self, count):

        self.define_player(count)
        return self.player


class Turn:

    def __init__(self, player, challenge):
        self.player = player
        self.challenge = challenge

    def return_turn(self, if_target):

        if if_target:
            self.challenge['Стоит ли пробовать'] = self.simulate_turn()

        return pd.DataFrame(self.player).T.merge(pd.DataFrame(self.challenge).T, how='cross')

    def count_rune_probability(self, main, extra, threshold):
        # Количество рун, которые могут быть 0 или 1
        n1 = 3
        # Количество рун, которые могут быть 1 или 2
        n2 = main + extra

        # Вычислим вероятности для первой группы рун (0 или 1)
        prob1 = {}
        for k1 in range(n1 + 1):  # k1 - количество единиц среди 3 рун
            # Вероятность получить k1 единиц
            p1 = comb(n1, k1) * (0.5 ** n1)
            # Сумма для k1 единиц: k1 * 1 + (n1 - k1) * 0 = k1
            sum1 = k1
            prob1[sum1] = p1

        # Вычислим вероятности для второй группы рун (1 или 2)
        prob2 = {}
        for k2 in range(n2 + 1):  # k2 - количество двоек среди (main + extra) рун
            # Вероятность получить k2 двоек
            p2 = comb(n2, k2) * (0.5 ** n2)
            # Сумма для k2 двоек: k2 * 2 + (n2 - k2) * 1 = k2 + n2
            sum2 = k2 + n2
            prob2[sum2] = p2

        # Переберем все возможные комбинации сумм и найдем вероятность
        total_prob = 0
        for sum1 in prob1:
            for sum2 in prob2:
                if (sum1 + sum2) >= threshold:
                    total_prob += prob1[sum1] * prob2[sum2]

        return total_prob

    def simulate_turn(self):
        main_rune = 0
        extra_rune = 0

        self.player['Цель'] = [self.player['Цель_1'],self.player['Цель_2'],self.player['Цель_3']]
        self.player['Руны'] = [self.player['Руна_1'], self.player['Руна_2']]

        if self.challenge['Основная руна'] in self.player['Руны']:
            main_rune += 1

        if self.challenge['Дополнительная руна'] in self.player['Руны']:
            main_rune += 1

        if self.player['Опыт'] > 0 and self.player['Опция'] in [self.challenge['Основная руна'], self.challenge['Дополнительная руна']]:
            extra_rune = 1

        rune_prob = self.count_rune_probability(main_rune, extra_rune, 
                                                self.challenge['Сложность'])

        if rune_prob >= 0.4 and rune_prob < 0.65 and self.challenge['Основная руна'] in self.player['Цель']:
            return 1
        elif rune_prob >= 0.65:
            return 1
        else:
            return 0


class Initial_data():

    def __init__(self):
   
        self.first_cards = pd.read_csv('.first_card.csv', sep=';')
        self.second_cards = pd.read_csv('second_card.csv', sep=';')
        self.third_cards = pd.read_csv('third_card.csv', sep=';')
        self.challenges = pd.read_csv('challenge.csv', sep=';')

    def define_all_players(self):

        players_list = []
        count = 1
        for i in range(len(self.first_cards)):
            for j in range(len(self.second_cards)):
                for k in range(len(self.third_cards)):
                    current_player = Player(self.first_cards.iloc[i], 
                                            self.second_cards.iloc[j], 
                                            self.third_cards.iloc[k], 
                                            0).return_player(count)
                    players_list.append(current_player)
                    count += 1
                    current_player = Player(self.first_cards.iloc[i], 
                                            self.second_cards.iloc[j], 
                                            self.third_cards.iloc[k], 
                                            1).return_player(count)
                    players_list.append(current_player)
                    count += 1

        self.players = pd.DataFrame(players_list)

    def define_turns(self, count, if_target): 

        self.define_all_players()
        turns_list = pd.DataFrame()
        for i in range(count):
            turn = Turn(self.players.sample(1).iloc[0], self.challenges.sample(1).iloc[0])
            turns_list = pd.concat([turns_list, turn.return_turn(if_target)], axis=0)

        self.turns = pd.DataFrame(turns_list)
        return self.turns


# if __name__ == "__main__":

data = Initial_data()
train_test_turns = data.define_turns(1000, True)
print(train_test_turns.head())
