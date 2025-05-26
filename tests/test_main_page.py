import time
import pytest
from pages.main_page import MainPage, MainPageLocators
from selenium.webdriver.common.by import By


def test_add_and_delete_trainer(browser) -> None:
    main_page = MainPage(browser)
    try:
        main_page.open_main_page()
        main_page.fill_input_field(MainPageLocators.ADD_TRAINER_INPUT, 'Лера')
        main_page.element_click(MainPageLocators.ADD_TRAINER_BUTTON)
        assert main_page.check_element_is_visible((By.XPATH, "//li[text()='Лера ']")) is not False, "Тренер не добавлен"
    finally:
        main_page.delete_trainer_or_workout_element("Лера ")
        time.sleep(0.5)
        assert main_page.check_element_is_visible((By.XPATH, "//li[text()='Лера ']")) is False, "Тренер не удален"


@pytest.mark.smoke
def test_add_and_delete_workout(browser) -> None:
    main_page = MainPage(browser)
    try:
        main_page.open_main_page()
        main_page.fill_input_field(MainPageLocators.ADD_WORKOUT_INPUT, 'Растяжка с подкачкой')
        main_page.element_click(MainPageLocators.ADD_WORKOUT_BUTTON)
        assert (main_page.check_element_is_visible((By.XPATH, "//li[text()='Растяжка с подкачкой ']"))
                is not False), "Тренировка не добавлена"
    finally:
        main_page.delete_trainer_or_workout_element("Растяжка с подкачкой ")
        time.sleep(0.5)
        assert (main_page.check_element_is_visible((By.XPATH, "//li[text()='Растяжка с подкачкой ']"))
                is False), "Тренировка не удалена"


def test_show_workout_table(browser) -> None:
    main_page = MainPage(browser)
    main_page.open_main_page()
    main_page.click_show_schedule_button()
    time.sleep(0.5)
    assert (main_page.check_element_is_visible(MainPageLocators.VALIDATION_MESSAGE)
            is not False), "Валлидационное сообщение отсутствует"
    main_page.select_month(1)
    main_page.click_show_schedule_button()
    main_page.take_screenshot()
    assert main_page.table_is_visible() is not False, "Расписание не загружено"


def test_download_schedule_file(browser) -> None:
    main_page = MainPage(browser)
    main_page.open_main_page()
    main_page.click_download_schedule_button()
    time.sleep(1)
    main_page.take_screenshot()
    assert main_page.is_file_in_downloads('Расписание_тренировок.xlsx') is True, "Файл не скачан"


def test_play_music_in_iframe(browser) -> None:
    main_page = MainPage(browser)
    main_page.open_main_page()
    time.sleep(2)
    main_page.play_music()
    time.sleep(10)
    main_page.take_screenshot()
    assert main_page.progress_bar_value() > 0, "Музыка не запустилась"


def test_create_schedule(browser) -> None:
    main_page = MainPage(browser)
    main_page.open_main_page()
    time.sleep(2)
    main_page.change_trainer_color(0, 'ff5733')
    main_page.change_trainer_color(1, '8633ff')
    main_page.select_month(1)
    main_page.add_row()
    main_page.select_time(0, '9:00 - 10:00')
    assert main_page.check_disable_status_of_save_button() is True, "Кнопка 'Сохранить созданное расписание' активна"
    main_page.fill_cells()
    assert main_page.check_disable_status_of_save_button() is False, "Кнопка 'Сохранить созданное расписание' неактивна"
    main_page.add_row()
    main_page.select_time(1, '10:00 - 11:00')
    assert main_page.check_disable_status_of_save_button() is True, "Кнопка 'Сохранить созданное расписание' активна"
    main_page.fill_cells(2)
    assert main_page.check_disable_status_of_save_button() is False, "Кнопка 'Сохранить созданное расписание' неактивна"
    main_page.add_row()
    assert main_page.check_disable_status_of_save_button() is True, "Кнопка 'Сохранить созданное расписание' активна"
    main_page.delete_row(3)
    assert main_page.check_disable_status_of_save_button() is False, "Кнопка 'Сохранить созданное расписание' неактивна"
    main_page.click_save_schedule_button()
    assert (main_page.check_element_is_visible(MainPageLocators.SUCCESS_SAVE_MODAL_WINDOW)
            is True), "Расписание не сохранено"
    main_page.take_screenshot()
    main_page.element_click(MainPageLocators.CLOSING_MODAL_BUTTON)
    assert (main_page.check_element_is_visible(MainPageLocators.SUCCESS_SAVE_MODAL_WINDOW)
            is False), "Модальное окно не закрыто"
