from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import pandas as pd
from prettytable import PrettyTable
import time

# Считываем данные с flashscore возвращаем данные со страницы с live-матчами
def read_web_page():
    url = "https://www.flashscorekz.com/table-tennis/"
    geckodriver_path = r'D:\src_git\flashscore parse\firefoxdriver\geckodriver.exe'

    #url = 'https://tennis-score.pro/live_v2/' #Лига ПРО

    service = Service(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=service)
    driver.get(url)

    time.sleep(3)

    # Находим все текущие live-матчи
    data_rows = driver.find_elements("xpath", "//div[@class='event__match event__match--live event__match--twoLine']")

    return data_rows


# Заполняем таблицу с результатами матчей
def get_dataframe(data_rows):

    print('Количество лайв-матчей:', len(data_rows), '\n')

    # Список полей
    # Текущий сет (Пример вывода: 3)
    cur_set = []
    # Игрок 1 (Пример вывода: Ivanov I.)
    participant_home = []
    # Игрок 2 (Пример вывода: Иванов И.)
    participant_away = []
    # Количество выигранных сетов 1-ого игрока (Пример вывода: 3)
    score_home = []
    # Количество выигранных сетов 2-ого игрока (Пример вывода: 2)
    score_away = []
    # Игрок 1: число очков в 1-м сете
    points_home_1_set = []
    # Игрок 2: число очков в 1-м сете
    points_away_1_set = []
    # Игрок 1: число очков в 2-м сете
    points_home_2_set = []
    # Игрок 2: число очков в 2-м сете
    points_away_2_set = []
    # Игрок 1: число очков в 3-м сете
    points_home_3_set = []
    # Игрок 2: число очков в 3-м сете
    points_away_3_set = []
    # Игрок 1: число очков в 4-м сете
    points_home_4_set = []
    # Игрок 2: число очков в 4-м сете
    points_away_4_set = []
    # Игрок 1: число очков в 5-м сете
    points_home_5_set = []
    # Игрок 2: число очков в 5-м сете
    points_away_5_set = []

    for row in data_rows:
        # Игрок 1 (Пример вывода: Иванов А.)
        participant_home.append(row.find_element("xpath",
                                            ".//div[@class='event__participant event__participant--home']").text)
        # Игрок 2 (Пример вывода: Иванов И.)
        participant_away.append(row.find_element("xpath",
                                            ".//div[@class='event__participant event__participant--away']").text)
        # Количество выигранных сетов 1-ого игрока (Пример вывода: 3)
        score_home.append(int(row.find_element("xpath", ".//div[@class='event__score event__score--home']").text))
        # Количество выигранных сетов 2-ого игрока (Пример вывода: 2)
        score_away.append(int(row.find_element("xpath", ".//div[@class='event__score event__score--away']").text))

        # Текущий сет (Пример вывода: 3-й сет) (достаем из строки только номер текущего сета)
        # Так как это поле может содержать значение "Ожидание обновления", то в этом случае номер
        # текущего сета определяем на основе количества выигранных сетов
        num_cur_set = 0
        try:
            num_cur_set = int(row.find_element("xpath", ".//div[@class='event__stage']").text[0])
        except Exception:
            num_cur_set = score_home[-1] + score_away[-1] + 1
        cur_set.append(num_cur_set)

        #for num_set in range(1, num_cur_set + 1): # сделать как-то через цикл
            #locals()["points_home_" + str(num_set) + "_set"].append(...)

        # 1 сет игрок 1
        try:
            points_home_1_set.append(int(row.find_element("xpath",
                                    ".//div[@class='event__part event__part--home event__part--1']").text))
        except Exception:
            points_home_1_set.append(0)

        # 1 сет игрок 2
        try:
            points_away_1_set.append(int(row.find_element("xpath",
                                    ".//div[@class='event__part event__part--away event__part--1']").text))
        except Exception:
            points_away_1_set.append(0)

        # 2 сет игрок 1
        try:
            points_home_2_set.append(int(row.find_element("xpath",
                                    ".//div[@class='event__part event__part--home event__part--2']").text))
        except Exception:
            points_home_2_set.append(0)

        # 2 сет игрок 2
        try:
            points_away_2_set.append(int(row.find_element("xpath",
                                    ".//div[@class='event__part event__part--away event__part--2']").text))
        except Exception:
            points_away_2_set.append(0)

        # 3 сет игрок 1
        try:
            points_home_3_set.append(int(row.find_element("xpath",
                                    ".//div[@class='event__part event__part--home event__part--3']").text))
        except Exception:
            points_home_3_set.append(0)

        # 3 сет игрок 2
        try:
            points_away_3_set.append(int(row.find_element("xpath",
                                    ".//div[@class='event__part event__part--away event__part--3']").text))
        except Exception:
            points_away_3_set.append(0)

        # 4 сет игрок 1
        try:
            points_home_4_set.append(int(row.find_element("xpath",
                                    ".//div[@class='event__part event__part--home event__part--4']").text))
        except Exception:
            points_home_4_set.append(0)

        # 4 сет игрок 2
        try:
            points_away_4_set.append(int(row.find_element("xpath",
                                    ".//div[@class='event__part event__part--away event__part--4']").text))
        except Exception:
            points_away_4_set.append(0)

        # 5 сет игрок 1
        try:
            points_home_5_set.append(int(row.find_element("xpath",
                                    ".//div[@class='event__part event__part--home event__part--5']").text))
        except Exception:
            points_home_5_set.append(0)

        # 5 сет игрок 2
        try:
            points_away_5_set.append(int(row.find_element("xpath",
                                    ".//div[@class='event__part event__part--away event__part--5']").text))
        except Exception:
            points_away_5_set.append(0)

    d = {"cur_set": cur_set,
         "participant_home": participant_home,
         "participant_away": participant_away,
         "score_home": score_home,
         "score_away": score_away,
         "points_home_1_set": points_home_1_set,
         "points_away_1_set": points_away_1_set,
         "points_home_2_set": points_home_2_set,
         "points_away_2_set": points_away_2_set,
         "points_home_3_set": points_home_3_set,
         "points_away_3_set": points_away_3_set,
         "points_home_4_set": points_home_4_set,
         "points_away_4_set": points_away_4_set,
         "points_home_5_set": points_home_5_set,
         "points_away_5_set": points_away_5_set}
    df = pd.DataFrame(d)

    #print(df) # вывод обрезанной части датафрейма
    #print(df.to_string()) # полный вывод датафрейма

    # Возвращаем датафрейм
    return df

# Вывести в консоль данные по матчам в виде таблицы
# Пример вывода:
# +-----+-----------+---+----+----+----+----+----+
# | Cет |           | С |  1 |  2 |  3 |  4 |  5 |
# |-----+-----------+---+----+----+----+----+----|
# |  5  | Иванов И. | 2 | 11 |  9 | 11 |  8 |  8 |
# |     | Иванов П. | 2 |  9 | 11 |  7 | 11 |  5 |
# +-----+-----------+---+----+----+----+----+----+
def print_matchs_from_dataframe(dataframe):

    for index, df in dataframe.iterrows():

        my_table = PrettyTable()
        my_table.field_names = ["Сет", " ", "С", "1", "2", "3", "4", "5"]

        my_table.add_row([df['cur_set'], df['participant_home'], df['score_home'],
                          df['points_home_1_set'], df['points_home_2_set'],
                          df['points_home_3_set'], df['points_home_4_set'],
                          df['points_home_5_set']])
    
        my_table.add_row([ " ", df['participant_away'], df['score_away'],
                          df['points_away_1_set'], df['points_away_2_set'],
                          df['points_away_3_set'], df['points_away_4_set'],
                          df['points_away_5_set']])

        print(my_table, '\n')


def main():
    # Считываем данные с flashscore возвращаем данные со страницы с live-матчами
    data_rows = read_web_page()
    # Получаем датафрейм с данными лайв-матчей в настольном теннисе
    df = get_dataframe(data_rows)
    # Печатаем каждый матч из датафрейма в виде таблицы
    print_matchs_from_dataframe(df)

if __name__ == '__main__':
    main()
