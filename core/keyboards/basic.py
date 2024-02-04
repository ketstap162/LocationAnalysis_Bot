from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="",
        keyboard=[
            [KeyboardButton(text="/report")],
        ]
    )


def get_locations_keyboard(locations: list[str]) -> ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()

    for location in locations:
        keyboard_builder.button(text=location)

    keyboard_builder.adjust(2, 2, 1)

    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Обери місто",
    )


class AnswersKeyboard:
    answer_ok = "Все чисто"
    answer_comment = "Залишити коментар"

    @classmethod
    def get_keyboard(cls):
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="",
            keyboard=[
                [
                    KeyboardButton(text=cls.answer_ok),
                    KeyboardButton(text=cls.answer_comment)
                ],
            ]
        )
        return keyboard


class SkipPictureKeyboard:
    text = "Далі"

    @classmethod
    def get_keyboard(cls):
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="",
            keyboard=[
                [
                    KeyboardButton(text=cls.text),
                ],
            ]
        )
        return keyboard


class ReportKeyboard:
    report_view = "Показати звіт"
    report_send = "Відправити звіт"

    @classmethod
    def get_keyboard(cls):
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="",
            keyboard=[
                [
                    KeyboardButton(text=cls.report_view),
                    KeyboardButton(text=cls.report_send),
                ],
            ]
        )
        return keyboard
