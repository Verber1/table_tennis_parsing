from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import pandas as pd
from prettytable import PrettyTable
import time
import io

# Путь к расположению firefoxdriver для использования в selenium
geckodriver_path = r'D:\src_git\flashscore parse\firefoxdriver\geckodriver.exe'
# Флаг, сообщающий о том, что парсинг будет осуществляться с сайта flashscore,
# в ином случае парсить будем с сайта tennis-score.pro
is_parse_flashscore = False
# Максимальное число сетов (устанавливаем 7, так как встречаются матчи с 7-ю сетами)
max_set = 7
# Создаем датафрейм, который хранит в себе имена игроков из матча с нужным результатом
# Это нужно для того, чтобы по несколько раз не выводить данные по матчу,
# так как данные по игре с нужным результатом должны выводиться только один раз, чтобы не было СПАМа
df_with_need_result_game = pd.DataFrame(columns=['player_home', 'player_away'])

# Турниры, игры в которых не рассматриваем (нет ставок на матчи в этих турнирах)
#block_tournament = ['Мастерс', 'TSC Pro', 'Pro Spin Series']
block_tournament = ['1223232']

# Считываем данные с сайтов flashscore или tennis-score
def read_web_page():

    url = ''
    if is_parse_flashscore:
        url = 'https://www.flashscorekz.com/table-tennis/' # Нет результатов по российским лигам
    else:
        url = 'https://tennis-score.pro/live_v2/data.php' # Есть результаты по российским лигам

    service = Service(executable_path=geckodriver_path)
    options = Options()
    options.add_argument('--headless') # запускаем браузер в фоновом режиме (без интерфейса)
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)

    time.sleep(3)

    data_rows = []
    # Находим все текущие live-матчи, если парсим с flashscore
    if is_parse_flashscore:
        data_rows = driver.find_elements("xpath", "//div[@class='event__match event__match--live event__match--twoLine']")

    return driver, data_rows


# Заполняем таблицу с результатами матчей по данным с сайта flashscore
def get_dataframe_from_flashscore(data_rows):

    print('Количество лайв-матчей (flashscore):', len(data_rows), '\n')

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
    # Игрок 1: число очков в 6-м сете
    points_home_6_set = []
    # Игрок 2: число очков в 6-м сете
    points_away_6_set = []
    # Игрок 1: число очков в 7-м сете
    points_home_7_set = []
    # Игрок 2: число очков в 7-м сете
    points_away_7_set = []

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

        # Определяем количество выигранных очков в каждом сете для каждого игрока
        # Пример запроса:
        # Получить количество выигранных очков 1-ого игрока во 2 сете:
        #row.find_element("xpath",
        #                 ".//div[@class='event__part event__part--home event__part--2']").text)
        # Может возникнуть ситуация, когда во время обновления очков на сайте для одного из игроков
        # для текущего сета название @class немного изменяется (к нему добавляется "highlighted")
        # То есть, например, вместо @class='event__part event__part--home event__part--2' может быть
        #                           @class='event__part event__part--home highlighted event__part--2'
        # Этот момент тоже нужно учитывать, иначе возникнет ошибка
        str_home_begin = ".//div[@class=\'event__part event__part--home "
        str_away_begin = ".//div[@class=\'event__part event__part--away "
        str_middle = "event__part--"
        str_addition = "highlighted "
        str_ending = "\']"
        for num_set in range(1, num_cur_set + 1):
            points_home = 0
            points_away = 0
            str_end_tmp = str_middle + str(num_set) + str_ending

            try:
                str_home_temp = str_home_begin + str_end_tmp
                points_home = int(row.find_element("xpath", str_home_temp).text)
            except Exception:
                # Если получили исключение - добавляем "highlighted" к названию класса
                str_home_add = str_home_begin + str_addition + str_end_tmp
                points_home = int(row.find_element("xpath", str_home_add).text)

            try:
                str_away_temp = str_away_begin + str_end_tmp
                points_away = int(row.find_element("xpath", str_away_temp).text)
            except Exception:
                # Если получили исключение - добавляем "highlighted" к названию класса
                str_away_add = str_away_begin + str_addition + str_end_tmp
                points_away = int(row.find_element("xpath", str_away_add).text)

            locals()["points_home_" + str(num_set) + "_set"].append(points_home)
            locals()["points_away_" + str(num_set) + "_set"].append(points_away)

        # Заполняем счёт в оставшихся сетах 0, так как данные по еще не начатым сетам
        # мы не можем прочитать
        for num_set in range(num_cur_set + 1, max_set + 1):
            locals()["points_home_" + str(num_set) + "_set"].append(0)
            locals()["points_away_" + str(num_set) + "_set"].append(0)

    # Собираем получившиеся поля в один список
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
         "points_away_5_set": points_away_5_set,
         "points_home_6_set": points_home_6_set,
         "points_away_6_set": points_away_6_set,
         "points_home_7_set": points_home_7_set,
         "points_away_7_set": points_away_7_set}

    # Создаем из списка датафрейм
    df = pd.DataFrame(d)

    #print(df) # вывод обрезанной части датафрейма
    #print(df.to_string()) # полный вывод датафрейма

    # Возвращаем датафрейм
    return df

# Заполняем таблицу с результатами матчей по данным с сайта tennis-score
def get_dataframe_from_tennis_score(driver):

    data_rows = driver.find_elements("xpath", "//*[@class='table align-middle bg-white overflow-hidden']/tbody/tr")
    num_matches = len(data_rows)

    # Текущее время
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    print(current_time, 'Количество лайв-матчей (tennis-score):', num_matches)

    # Список полей
    # Название турнира (Пример вывода: Лига Про)
    tournament_name = []
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
    # Игрок 1: число очков в 6-м сете
    points_home_6_set = []
    # Игрок 2: число очков в 6-м сете
    points_away_6_set = []
    # Игрок 1: число очков в 7-м сете
    points_home_7_set = []
    # Игрок 2: число очков в 7-м сете
    points_away_7_set = []

    # Данные по матчам берём напрямую из таблицы, обращаясь к элементам таблицы через индексы
    # Итерироваться по строкам (матчам) нужно с индекса tr[1]
    # Столбец с игроками можно получить по индексу td[2]
    # Столбец со счётом можно получить по индексу td[3]
    # Столбец с названием турнира можно получить по индексу td[12]
    for match in range(1, num_matches + 1):

        # Находим название турнира, в рамках которого играется матч, и смотрим, нет ли этого
        # турнира в списке заблокированных. Если этот турнир входит в список заблокированных,
        # тогда этот матч не учитываем
        tournament = driver.find_elements("xpath", "//*[@class= "
                                                   "'table align-middle bg-white overflow-hidden']"
                                                   "/tbody/tr[" + str(match) + "]/td[12]")[0].text
        find_block_tournament = False
        for block_t in block_tournament:
            if tournament.find(block_t) != -1:
                find_block_tournament = True
                break

        if find_block_tournament:
            continue

        tournament_name.append(tournament)

        # Находим строку с очками по каждому сету, а также количество выигранных сетов
        # Строка с очками приходит в следующем виде:
        # '2 '\n' 11 '\n' 5 '\n' 11 '\n' 3 '\n' 1 '\n' 4 '\n' 11 '\n' 8 '\n' 2 '\n' 55'
        # Последнее число в строке означает сумму всех выигранных очков
        # Расшифровывается строка так:
        # +---+----+----+----+----+
        # | С |  1 |  2 |  3 |  4 |
        # +---+----+----+----+----+
        # | 2 | 11 |  5 | 11 |  3 |
        # | 1 |  4 | 11 |  8 |  2 |
        # +---+----+----+----+----+
        # ([0] используем потому что возвращается список, но в списке по индексу [1] ничего нет,
        # вся информация находится в элементе с индексом [0])
        points_str = driver.find_elements("xpath", "//*[@class= "
                                                   "'table align-middle bg-white overflow-hidden']"
                                                   "/tbody/tr[" + str(match) + "]/td[3]")[0].text
        # Создаем из строки с очками список
        points = points_str.split('\n')
         # Удаляем значение с суммой всех выигранных очков
        del points[-1]
        # Определяем номер текущего сета
        num_cur_set = int((len(points) - 2) / 2)
        cur_set.append(num_cur_set)
        # Разбиваем список на два списка (очки для каждого игрока)
        points_home_str = points[:len(points) // 2]
        points_away_str = points[len(points) // 2:]
        # Сохраняем число выигранных сетов кадым игроком
        score_home.append(int(points_home_str[0]))
        score_away.append(int(points_away_str[0]))
        # Удаляем число выигранных сетов кадым игроком из списка
        del points_home_str[0]
        del points_away_str[0]
        # Заполняем список с выигранными очками по каждому сету для каждого игрока
        for num_set in range(1, num_cur_set + 1):
            idx = num_set - 1
            locals()["points_home_" + str(num_set) + "_set"].append(int(points_home_str[idx]))
            locals()["points_away_" + str(num_set) + "_set"].append(int(points_away_str[idx]))

        # Заполняем счёт в оставшихся сетах 0, так как данные по еще не начатым сетам
        # мы не можем прочитать

        for num_set in range(num_cur_set + 1, max_set + 1):
            locals()["points_home_" + str(num_set) + "_set"].append(0)
            locals()["points_away_" + str(num_set) + "_set"].append(0)

        # Находим строку с игроками
        # Строка с игроками приходит в следующем виде:
        # 'Иванов Иван (Рос) '\n' Петров Петр (Рос)'
        # ([0] используем потому что возвращается список, но в списке по индексу [1] ничего нет,
        # вся информация находится в элементе с индексом [0])
        players_str = driver.find_elements("xpath", "//*[@class= "
                                                    "'table align-middle bg-white overflow-hidden']"
                                                    "/tbody/tr[" + str(match) + "]/td[2]")[0].text
        # Создаем из строки с игроками список
        players = players_str.split('\n')
        participant_home.append(players[0])
        participant_away.append(players[1])

    print('Из них рассматриваем только', len(tournament_name), 'матчей')

    # Собираем получившиеся поля в один список
    d = {"tournament_name": tournament_name,
         "cur_set": cur_set,
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
         "points_away_5_set": points_away_5_set,
         "points_home_6_set": points_home_6_set,
         "points_away_6_set": points_away_6_set,
         "points_home_7_set": points_home_7_set,
         "points_away_7_set": points_away_7_set}

    # Создаем из списка датафрейм
    df = pd.DataFrame(d)

    # print(df) # вывод обрезанной части датафрейма
    # print(df.to_string()) # полный вывод датафрейма

    # Возвращаем датафрейм
    return df

# Анализируем датафрейм на предмет подходящих для ставки матчей
# (ищем матч, в котором 3 последних сета подряд заканчиваются с одинаковым счётом)
def dataframe_analysis(dataframe):

    # Список матчей для вывода в текстовом формате
    output_text_res = []

    # Итерируемся по матчам
    for index, df in dataframe.iterrows():

        # Номер текущего сета
        num_cur_set = df['cur_set']

        # Если текущий сет меньше 4, значит в этом матче еще не может быть
        # ситуации, когда 3 последних сета подряд заканчиваются с одинаковым счётом
        # Поэтому такой матч не рассматриваем
        if num_cur_set < 4:
            continue

        # Сумма очков в текущем раунде
        sum_points_cur_set = df['points_home_' + str(num_cur_set) + '_set'] \
                           + df['points_away_' + str(num_cur_set) + '_set']

        # Также если в текущем сете было разыграно больше 3-х очков, то такой матч тоже
        # не рассматриваем, потому что даже если прошлые три сета закончились с одинаковым счётом,
        # то мы уже не успеем сделать ставку, что этот сет закончится с другим счётом
        if sum_points_cur_set > 3:
            continue

        # Номер предыдущего сета
        num_prev_set = num_cur_set - 1
        # Для поиска игр, в которых 3 последних сета подряд заканчиваются с одинаковым счётом
        # будем сравнивать разницу очков за сет, а также максимальное количество очков, набранное за сет
        delta_points = int(abs(df['points_home_' + str(num_prev_set) + '_set'] \
                             - df['points_away_' + str(num_prev_set) + '_set']))

        max_points_in_set = int(max(df['points_home_' + str(num_prev_set) + '_set'],
                                    df['points_away_' + str(num_prev_set) + '_set']))

        # флаг означающий, что игра, в которой 3 последних сета подряд заканчиваются
        # с одинаковым счётом, был найден
        is_find_match = True
        
        # Итерируемся по оставшимся двум сетам
        for num_set in range(num_cur_set - 2, num_cur_set - 4, -1):

            # Находим дельту очков и максимум
            delta_p = int(abs(df['points_home_' + str(num_set) + '_set'] \
                            - df['points_away_' + str(num_set) + '_set']))

            max_p = int(max(df['points_home_' + str(num_set) + '_set'],
                            df['points_away_' + str(num_set) + '_set']))

            # Сравниваем значения. Если значения не совпадают - выходи из цикла и переходим к следующему матчу
            if delta_points != delta_p or max_points_in_set != max_p:
                is_find_match = False
                break

        # Если текущая игра, в которой 3 последних сета подряд заканчиваются
        # с одинаковым счётом, была найдена - выводим таблицу по ней,
        # если нет - переходим к следующей игре
        if is_find_match:
            # Проверяем, что данные по этой игре еще не выводилсь
            # Если данные уже выводилсь - больше не выводим
            if check_game_in_base(df['participant_home'], df['participant_away']) == False:
                out_val = print_match_from_dataframe(df)
                output_text_res.append(out_val)
        else:
            continue

    # Удаляем закончившиеся игры из базы, так как в этих игах уже нет надобности
    delete_completed_matches_from_base(dataframe)

    return output_text_res


# Вывести в консоль данные по матчам в виде таблицы
def print_matches_from_dataframe(dataframe):

    for index, df in dataframe.iterrows():
        print_match_from_dataframe(df)

# Вывести в консоль данные по конкретному матчу по строке из датафрейма
# Пример вывода:
# +-----+-----------+---+----+----+----+----+----+----+----+
# | Cет |           | С |  1 |  2 |  3 |  4 |  5 |  6 |  7 |
# |-----+-----------+---+----+----+----+----+----|----+----|
# |  5  | Иванов И. | 2 | 11 |  9 | 11 |  8 |  8 |  0 |  0 |
# |     | Иванов П. | 2 |  9 | 11 |  7 | 11 |  5 |  0 |  0 |
# +-----+-----------+---+----+----+----+----+----+----+----+
def print_match_from_dataframe(df):

    my_table = PrettyTable()
    my_table.field_names = ["Сет", " ", "С", "1", "2", "3", "4", "5", "6", "7"]

    # 1-ая строка таблицы
    my_table.add_row([df['cur_set'], df['participant_home'], df['score_home'],
                      df['points_home_1_set'], df['points_home_2_set'],
                      df['points_home_3_set'], df['points_home_4_set'],
                      df['points_home_5_set'], df['points_home_6_set'],
                      df['points_home_7_set']])

    # 2-ая строка таблицы
    my_table.add_row([" ", df['participant_away'], df['score_away'],
                      df['points_away_1_set'], df['points_away_2_set'],
                      df['points_away_3_set'], df['points_away_4_set'],
                      df['points_away_5_set'], df['points_away_6_set'],
                      df['points_away_7_set']])
    #print(df['tournament_name'])
    #print(my_table, '\n')
    # print(my_table, '\n', file=output)

    output = io.StringIO()
    print(df['tournament_name'], '\n', df['cur_set'], "-ый сет: ",
          df['participant_home'], ' ', df['score_home'], " - ",
          df['participant_away'], ' ', df['score_away'], ":", '\n',
          '(',df['points_home_1_set'], '-', df['points_away_1_set'], '), ',
          '(', df['points_home_2_set'], '-', df['points_away_2_set'], '), ',
          '(', df['points_home_3_set'], '-', df['points_away_3_set'], '), ',
          '(', df['points_home_4_set'], '-', df['points_away_4_set'], '), ',
          '(', df['points_home_5_set'], '-', df['points_away_5_set'], '), ',
          '(', df['points_home_6_set'], '-', df['points_away_6_set'], '), ',
          '(', df['points_home_7_set'], '-', df['points_away_7_set'], '), ',
          '\n', sep='', file=output)

    output_text_res = output.getvalue()
    return output_text_res

# Проверям, что найденная игра с нужным счётом еще не существует в базе, и если это так - добавляем игру в базу
def check_game_in_base(participant_home, participant_away):
    is_game_exists_in_base = False
    if (len(df_with_need_result_game)) > 0:
        for index, df in df_with_need_result_game.iterrows():
            if (df['player_home'] == participant_home) & (df['player_away'] == participant_away):
                is_game_exists_in_base = True

    # Если игра не была найдена в базе - добавляем её туда
    if is_game_exists_in_base == False:
        df_with_need_result_game.loc[len(df_with_need_result_game.index)] = [participant_home, participant_away]
        print("Игра ", participant_home, " - ", participant_away, " была добавлена в список игр! Размер списка: ",
              len(df_with_need_result_game), sep="")

    return is_game_exists_in_base

# Удалить закончившиеся игры из базы, так как в этих игах уже нет надобности
def delete_completed_matches_from_base(dataframe_live):
    if (len(df_with_need_result_game)) == 0:
        return

    # Проходим по матчам в базе и смотрим, не осталось ли там матчей, которые уже закончились
    # (то есть этих матчей уже нет в списке live-матчей)
    list_idx = [] # индексы матчей в базе, которые уже закончились
    for idx_row_base, df_base in df_with_need_result_game.iterrows():
        is_live_match_find = False
        for idx_row_live, df_live in dataframe_live.iterrows():

            if (df_live['participant_home'] == df_base['player_home']) &\
               (df_live['participant_away'] == df_base['player_away']):
                is_live_match_find = True
                break

        if is_live_match_find == False:
            list_idx.append(idx_row_base)

    if len(list_idx) > 0:
        for idx in list_idx:
            try:
                print("Игра ", df_with_need_result_game['player_home'].loc[df_with_need_result_game.index[idx]], " - ",
                               df_with_need_result_game['player_away'].loc[df_with_need_result_game.index[idx]],
                    " была удалена из списка игр!", sep="")
            except Exception:
                print("Ошибка! Не могу вывести данные по удаленной игре")
                print("Текущая база:")
                print(df_with_need_result_game)
                print("Идекс строки базы, которую необходимо удалить:", idx)
        # Удаляем матчи из базы, которые уже закончились (нет в списке лайв-матчей)
        df_with_need_result_game.drop(list_idx, inplace=True)
        print("Список игр после удаления:", len(df_with_need_result_game))


def main():
    # Считываем данные с flashscore возвращаем данные со страницы с live-матчами
    driver, data_rows = read_web_page()
    # Получаем датафрейм с данными лайв-матчей в настольном теннисе
    df = []
    if is_parse_flashscore:
        df = get_dataframe_from_flashscore(data_rows)
    else:
        df = get_dataframe_from_tennis_score(driver)
    # Закрываем драйвер
    driver.quit()
    # Анализируем датафрейм на предмет подходящих для ставки матчей
    output_text_res = dataframe_analysis(df)
    # Печатаем каждый матч из датафрейма в виде таблицы
    #print_matches_from_dataframe(df)

    return output_text_res

# Тестирование функции для анализа игр
def test_work():
    # Список полей
    # Название турнира (Пример вывода: Лига Про)
    tournament_name = ['Лига Про']
    # Текущий сет (Пример вывода: 3)
    cur_set = [5]
    # Игрок 1 (Пример вывода: Ivanov I.)
    participant_home = ['Ivanov Ivan']
    # Игрок 2 (Пример вывода: Иванов И.)
    participant_away = ['Petrov Petr']
    # Количество выигранных сетов 1-ого игрока (Пример вывода: 3)
    score_home = [2]
    # Количество выигранных сетов 2-ого игрока (Пример вывода: 2)
    score_away = [2]
    points_home_1_set = [11]; points_away_1_set = [9]
    points_home_2_set = [8];  points_away_2_set = [11]
    points_home_3_set = [11]; points_away_3_set = [8]
    points_home_4_set = [8];  points_away_4_set = [11]
    points_home_5_set = [2];  points_away_5_set = [1]
    points_home_6_set = [0];  points_away_6_set = [0]
    points_home_7_set = [0];  points_away_7_set = [0]

    # Собираем получившиеся поля в один список
    d = {"tournament_name": tournament_name,
         "cur_set": cur_set,
         "participant_home": participant_home,   "participant_away": participant_away,
         "score_home": score_home,               "score_away": score_away,
         "points_home_1_set": points_home_1_set, "points_away_1_set": points_away_1_set,
         "points_home_2_set": points_home_2_set, "points_away_2_set": points_away_2_set,
         "points_home_3_set": points_home_3_set, "points_away_3_set": points_away_3_set,
         "points_home_4_set": points_home_4_set, "points_away_4_set": points_away_4_set,
         "points_home_5_set": points_home_5_set, "points_away_5_set": points_away_5_set,
         "points_home_6_set": points_home_6_set, "points_away_6_set": points_away_6_set,
         "points_home_7_set": points_home_7_set, "points_away_7_set": points_away_7_set}

    # Создаем из списка датафрейм
    df = pd.DataFrame(d)
    # Анализируем игру
    output_text_res = dataframe_analysis(df)

    return output_text_res

#if __name__ == '__main__':
    #main()
    #test_work()

