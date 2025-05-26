# Используем минимальный образ Python
FROM python:3.11-slim

# Устанавливаем зависимости ОС
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем переменные окружения для Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver


# Создаем рабочую директорию
WORKDIR /tests

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем тесты
COPY . .

# Устанавливаем allure-pytest
RUN pip install allure-pytest

# Команда по умолчанию: запускаем pytest с выводом в allure
CMD ["pytest", "--alluredir=/allure-results"]