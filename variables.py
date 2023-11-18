import configparser

# Создание конфигурации
config = configparser.ConfigParser()

# Чтение файла конфигурации
config.read('config.ini')

# Получение данных из файла конфигурации
TOKEN_BOT = config.get('Settings', 'TOKEN_BOT') # Токен бота
CHAT_ID = [int(x) for x in config.get('Settings', 'CHAT_ID').split(',')] # Список чатов, в которые отправляем результаты
WEB_DRIVER_PATH = config.get('Settings', 'WEB_DRIVER_PATH') # Путь к chromedriver.exe для использования в selenium

#print(f'TOKEN_BOT: {TOKEN_BOT}')
#print(f'CHAT_ID: {CHAT_ID}')
#print(f'WEB_DRIVER_PATH: {WEB_DRIVER_PATH}')