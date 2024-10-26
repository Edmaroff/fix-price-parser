import os

from dotenv import load_dotenv

# Название и модули проекта
BOT_NAME = "app"
SPIDER_MODULES = ["app.spiders"]
NEWSPIDER_MODULE = "app.spiders"

# Основные URL проекта
ALLOWED_DOMAINS = ["fix-price.com"]
START_URLS = [
    "https://fix-price.com/catalog/kosmetika-i-gigiena/gigienicheskie-sredstva",
    "https://fix-price.com/catalog/kosmetika-i-gigiena/ukhod-za-polostyu-rta",
    "https://fix-price.com/catalog/dlya-doma/aksessuary-dlya-odezhdy",
]


ROBOTSTXT_OBEY = False  # Для игнорирования robots.txt
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# Куки и настройки региона
COOKIES_ENABLED = True
COOKIES = {
    "locality": "%7B%22city%22%3A%22%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D"
    "1%80%D0%B3%22%2C%22cityId%22%3A55%2C%22longitude%22%3A60.597474%2C%22latitude%22"
    "%3A56.838011%2C%22prefix%22%3A%22%D0%B3%22%7D"
}

# Настройки Proxy
load_dotenv()

PROXY_USER = os.getenv("PROXY_LOGIN")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")
PROXY_IP = os.getenv("PROXY_IP")
PROXY_PORT = os.getenv("PROXY_PORT")

PROXY_ADDRESS = (
    f"http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_IP}:{PROXY_PORT}"
    if all([PROXY_USER, PROXY_PASSWORD, PROXY_IP, PROXY_PORT])
    else None
)

# Логирование
LOG_LEVEL = "INFO"  # INFO для стандартных логов
LOGSTATS_INTERVAL = 60  # Вывод статистики каждые 60 секунд

# Настройки экспорта
FEED_EXPORT_ENCODING = "utf-8"
FEED_FORMAT = "json"  # Формат выходных данных
FEED_URI = "output/%(name)s_%(time)s.json"  # Автоматически формируем имя файла

# Настройки Fingerprint
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
