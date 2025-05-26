FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl unzip gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Добавляем репозиторий Google Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Устанавливаем нужный ChromeDriver вручную
ARG CHROMEDRIVER_VERSION=136.0.7103.113
RUN curl -SL "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -o chromedriver.zip \
    && unzip chromedriver.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver.zip

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PYTHONPATH=/tests

WORKDIR /tests

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install allure-pytest

COPY . .

CMD ["pytest", "tests", "--alluredir=/allure-results"]
