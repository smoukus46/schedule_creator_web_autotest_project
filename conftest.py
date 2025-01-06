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
    options.page_load_strategy = 'eager'
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    browser.maximize_window()

    yield browser
    browser.quit()
