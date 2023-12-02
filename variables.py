import configparser

# Создание конфигурации
config = configparser.ConfigParser()

# Чтение файла конфигурации
config.read('config.ini')

# Получение данных из файла конфигурации
TOKEN_BOT = config.get('Settings', 'TOKEN_BOT') # Токен бота
CHAT_ID = [int(x) for x in config.get('Settings', 'CHAT_ID').split(',')] # Список чатов, в которые отправляем результаты
WEB_DRIVER_PATH = config.get('Settings', 'WEB_DRIVER_PATH') # Путь к chromedriver.exe для использования в selenium
OPERATING_SYSTEM = config.get('Settings', 'OPERATING_SYSTEM') # Операционнная система, на которой запускается скрипт (Windows или Linux)
TIME_PAUSE = int(config.get('Settings', 'TIME_PAUSE')) # Время паузы (sleep) (в секундах) между парсингом

#print(f'TOKEN_BOT: {TOKEN_BOT}')
#print(f'CHAT_ID: {CHAT_ID}')
#print(f'WEB_DRIVER_PATH: {WEB_DRIVER_PATH}')
#print(f'OPERATING_SYSTEM: {OPERATING_SYSTEM}')
#print(f'TIME_PAUSE: {TIME_PAUSE}')