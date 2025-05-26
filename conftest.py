import pytest
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Получаем абсолютный путь к корневой директории проекта
project_root = os.path.abspath(os.path.dirname(__file__))

# Добавляем корневую директорию в sys.path
sys.path.insert(0, project_root)


@pytest.fixture(scope="function")
def browser(request):

    options = Options()
    options.add_argument("--headless")  # ОБЯЗАТЕЛЬНО
    options.add_argument("--no-sandbox")  # ОБЯЗАТЕЛЬНО для Docker
    options.add_argument("--disable-dev-shm-usage")  # ОБЯЗАТЕЛЬНО для Docker
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.page_load_strategy = 'eager'
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    # Если запускается не в docker можно раскомментировать строку
    # browser.maximize_window()

    yield browser
    browser.quit()
