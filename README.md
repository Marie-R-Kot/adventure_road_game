# adventure_road_game
Данный проект преставляет собой симуляцию одного хода в игре "Дорога приключений", выбор 
и обучение моделя для предсказание стоит ли совершать этот ход или нет, а так же интерфейс 
для пользователя по получению предсказания модели

### Правила данного хода в игре

В начале хода у каждого игрока есть три карточки: слева направо - Происхождение, Стремление и Судьба. А так же возможно очки опыта(красные фишки)
Каждая из карточек обладает своими свойствами. 
Так на карточке происхождения указаны базовые руны доступные игроку. Всего есть шесть рун способностей:
Сила, Ловкость, Телосложение, Интеллект, Мудрость и Обаяние. На карточке происхождения указаны две доступные игроку.
Карточка стремления показывает может ли игрок потратить очки опыта и получить какую-либо дополнительную руну.
Карточка же судьбы определяет какие руны требуется собрать игроку для получения дополнительных очков в конце игры. 
Выбранный для данного проекта ход делается в самом начале игры, игрок решает какое испытание выбрать, чтобы приобрести новые или преумножить старые руны. 
Для прохождения испытания бросается набор из трех базовых рун, рун доступных для игрока солгасно его карточке происхождения и дополнительной руны согласно карточке стремлений. 
Важно отметить, что помимо основных рун, можно использовать только руны, указанные на карте испытания. 
Так, если на карточке испытания указаны руны Силы и Интеллекта, а у игрока на первой и второй карточках есть руны Силы и Ловкости. То он может использовать только руну Силы. 

Итак, что нужно сделать, чтобы преодолеть испытание:
1. Определите сложность испытания - это число указанное в левом верхнем углу карты. 
2. На карточке испытаний указано два варианта - сверху и снизу, игрок выбирает одиин из них, от этого зависит, какую руну он получить при успешном прохождении испытания. Нужно выбрать один из путей (вариантов). Если в описании пути есть знак +1, то сложность выбранного пути увеличивается на один соответственно.
3. Соберите доступные руны: три основных, руны способностей, имеющиеся у вашего персонажа и подходящие испытанию, и дополнительную руну, если она подходит испытанию и у вас есть очки опыта, которые можно обменять на нее. 
4. Бросьте руны. У каждой руны две стороны, в зависимости от того, какой стороной упала руна, она дает разное количество очков. Базовые руны могут дать ноль очков или одно, руны способностей - одно или два. 
5. Сложите все полученные очки, если сумма больше или равна сложности испытания, то вы его преодолели и можете забрать карточку себе

### Симуляция хода
Для обучения модели требовалось смоделировать достаточно большое количество ходов и ответов, стоит ли пытатьс пройти выбранное испытание. 
Для этого были перебраны все варианты комбинаций трех карт игрока и очков опыта. Затем из всех возможных игроков один выбрается случайно и составляет пару со случайным испытанием. 
Подсчитываются все руны способностей, которые может использовать игрок. И вычисляется вероятность преодолеть испытание согласно его сложности. 
Есть вероятность мала, то симуляция говорит, что данные ход не стоит того ни при каких обстоятельствах. 
Если вероятность средняя, но карточка испытания содержит целевую руну(одну из рун указанных на карте судьбы), то стоит рискнуть.
Если вероятность успеха высока, то не зависимо от приобретаемой руны стоит попытаться. 
Таким образом симуляция возвращается 1 - если стоит попробовать взять испытание и 0, если даже пытаться не стоит. 

### Модель 
Результаты полученные при симуляции хода используются для выбора и обучения модели, что подробно описано в файле model_choice. Он содержит небольшое исследование данных, их подготовку для обучения, выбор модели и поиск наилучших гиперпараметров

# Интерфейс
Файл main.py содержит небольшой интерфейс с выбором карт игрока, очков опыта и предполагаемого испытания, а так же форму вывода предсказания модели. 
