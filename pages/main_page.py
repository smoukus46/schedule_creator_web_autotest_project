import random
import time
from pathlib import Path
import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class MainPageLocators:
    SHOW_SCHEDULE_BUTTON = (By.XPATH, "//div[@class='btn-div']/button[1]")
    SAVE_SCHEDULE_BUTTON = (By.XPATH, "//div[@class='btn-div']/button[2]")
    DOWNLOAD_SCHEDULE_BUTTON = (By.XPATH, "//div[@class='btn-div']/button[3]")
    ADD_TRAINER_INPUT = (By.CLASS_NAME, "add-trainer-input")
    ADD_TRAINER_BUTTON = (By.CLASS_NAME, "add-trainer")
    ADD_WORKOUT_INPUT = (By.CLASS_NAME, "add-workout-input")
    ADD_WORKOUT_BUTTON = (By.CLASS_NAME, "add-workout")
    ADD_ROW_BUTTON = (By.ID, "add-row-btn")
    TRAINER_LIST = (By.CSS_SELECTOR, "#trainerUL > li")
    WORKOUT_LIST = (By.CSS_SELECTOR, "#workoutUL > li")
    TRAINER_COLOR_INPUTS = (By.CSS_SELECTOR, "li > input")
    TIME_LIST = (By.TAG_NAME, "select")
    DATEPICKER_INPUT = (By.CLASS_NAME, "datepicker-input")
    YEAR_DISPLAY = (By.CLASS_NAME, "year-display")
    PREV_YEAR_BUTTON = (By.CLASS_NAME, "prev-year")
    NEXT_YEAR_BUTTON = (By.CLASS_NAME, "next-year")
    MONTHS_LIST = (By.CLASS_NAME, "month")
    TABLE_ROWS = (By.XPATH, "//tbody/tr")
    CELLS = (By.TAG_NAME, "td")
    MUSIC_IFRAME = (By.XPATH, "//iframe[@src='https://music.yandex.ru/iframe/playlist/nikita.yakovlev46/3']")
    SONGS = (By.XPATH, "//div[@class='container_trackContainer__mg6Bm']")
    PLAY_BUTTONS = (By.XPATH,
                    "(//button[@class='button_button__yEIr9 button_iframe-play-track__10LwV button_extra-small__M4y7J button_round__a9uX5'])")
    PROGRESS_BAR = (By.CLASS_NAME, "progress_progressTrack__D28nE")
    VALIDATION_MESSAGE = (By.CLASS_NAME, "validation-error")
    SUCCESS_SAVE_MODAL_WINDOW = (By.XPATH, "//div[text()='Данные успешно отправлены ']")
    CLOSING_MODAL_BUTTON = (By.ID, "closeModal")


class MainPage:
    def __init__(self, browser):
        self.browser = browser

    @allure.step("Открыть главную страницу")
    def open_main_page(self) -> None:
        self.browser.get('http://195.133.66.33:8000/')

    @allure.step("Заполнить поле")
    def fill_input_field(self, locator: tuple, value: str) -> None:
        self.browser.find_element(*locator).send_keys(value)

    def element_click(self, locator) -> None:
        wait = WebDriverWait(self.browser, 5, 1)
        wait.until(EC.element_to_be_clickable(locator)).click()

    def find_item(self, locator):
        wait = WebDriverWait(self.browser, 5, 1)
        return wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Проверить, что элемент отображается на странице")
    def check_element_is_visible(self, locator: tuple):
        try:
            self.find_item(locator)
            return True
        except TimeoutException:
            return False

    @allure.step("Удалить из списка значение")
    def delete_trainer_or_workout_element(self, elem_text: str) -> None:
        self.element_click((By.XPATH, f"//li[text()='{elem_text}']/button"))

    @allure.step("Проверить, что таблица отображается")
    def table_is_visible(self) -> bool:
        wait = WebDriverWait(self.browser, 10, 1)
        wait.until(EC.visibility_of_element_located(MainPageLocators.CELLS))

        cells = self.browser.find_elements(*MainPageLocators.CELLS)

        for cell in cells:
            cell_style = cell.get_attribute('style')
            if cell_style and "background-color" in cell_style:
                return True
            else:
                break

        return False

    @allure.step("Выбрать месяц")
    def select_month(self, month_index) -> None:
        self.element_click(MainPageLocators.DATEPICKER_INPUT)
        month_list = self.browser.find_elements(*MainPageLocators.MONTHS_LIST)
        month_list[month_index].click()

    @allure.step("Нажать кнопку 'Показать расписание за выбранный месяц'")
    def click_show_schedule_button(self) -> None:
        self.element_click(MainPageLocators.SHOW_SCHEDULE_BUTTON)

    @allure.step("Нажать кнопку 'Выгрузить файл с расписанием'")
    def click_download_schedule_button(self) -> None:
        self.element_click(MainPageLocators.DOWNLOAD_SCHEDULE_BUTTON)

    @allure.step("Проверить, что файл скачался в папку загрузок")
    def is_file_in_downloads(self, file_name: str) -> bool:
        download_path = Path.home() / 'Downloads'
        file_path = download_path / file_name
        print(file_path)
        print(file_path.is_file())
        print(file_path.exists())
        return file_path.is_file()

    @allure.step("Включить любую песню")
    def play_music(self) -> None:
        action = ActionChains(self.browser)
        frame = self.find_item(MainPageLocators.MUSIC_IFRAME)

        self.browser.switch_to.frame(frame)

        songs_list = self.browser.find_elements(*MainPageLocators.SONGS)
        music_list = self.browser.find_elements(*MainPageLocators.PLAY_BUTTONS)

        action.move_to_element(songs_list[0]).perform()
        time.sleep(1)
        self.browser.execute_script("arguments[0].click();", music_list[0])

    @allure.step("Проверить, что шкала воспроизведения песни заполняется")
    def progress_bar_value(self) -> float:
        progress_bar = self.browser.find_element(*MainPageLocators.PROGRESS_BAR)
        try:
            return float(progress_bar.get_attribute("style")[22:29])
        except ValueError:
            return 0

    @allure.step("Выбрать цвет для тренера")
    def change_trainer_color(self, trainer_index: int, hex_code: str) -> None:
        trainer = self.browser.find_elements(*MainPageLocators.TRAINER_COLOR_INPUTS)
        self.browser.execute_script(f"arguments[0].value = '#{hex_code}';", trainer[trainer_index])
        self.browser.execute_script("arguments[0].dispatchEvent(new Event('input'));", trainer[trainer_index])

    @allure.step("Добавить строку в таблицу, нажав '+'")
    def add_row(self) -> None:
        self.find_item(MainPageLocators.ADD_ROW_BUTTON).click()

    @allure.step("Удалить строку, нажав на 'Х'")
    def delete_row(self, row_index: int) -> None:
        self.find_item((By.XPATH, f"//tbody/tr[{row_index}]/button")).click()

    @allure.step("Заполнить ячейки")
    def fill_cells(self, row_index: int = 1) -> None:
        action = ActionChains(self.browser)
        trainer_list = self.browser.find_elements(*MainPageLocators.TRAINER_LIST)
        workout_list = self.browser.find_elements(*MainPageLocators.WORKOUT_LIST)
        cells = self.browser.find_elements(By.XPATH, f"//tbody/tr[{row_index}]/td")

        for cell in cells:
            action.drag_and_drop(trainer_list[random.randint(0, 1)], cell).perform()
            action.drag_and_drop(workout_list[random.randint(0, 1)], cell).perform()

    @allure.step("Выбрать время")
    def select_time(self, select_index: int, time_value: str) -> None:
        time_list = Select(self.browser.find_elements(*MainPageLocators.TIME_LIST)[select_index])
        time_list.select_by_value(time_value)

    @allure.step("Проверить, что кнопка 'Сохранить созданное расписание' неактивна")
    def check_disable_status_of_save_button(self) -> bool:
        if self.find_item(MainPageLocators.SAVE_SCHEDULE_BUTTON).get_attribute("disabled"):
            return True
        else:
            return False

    @allure.step("Нажать кнопку 'Сохранить созданное расписание'")
    def click_save_schedule_button(self) -> None:
        self.find_item(MainPageLocators.SAVE_SCHEDULE_BUTTON).click()

    @allure.step("Сделать скриншот")
    def take_screenshot(self) -> None:
        screenshot = self.browser.get_screenshot_as_png()
        allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
