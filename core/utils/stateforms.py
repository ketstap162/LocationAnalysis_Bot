from aiogram.fsm.state import StatesGroup, State


class ReportQuestionForm(StatesGroup):
    GET_ANSWER = State()
    GET_COMMENT = State()
    GET_PICTURE = State()


class ReportForm(StatesGroup):
    GET_LOCATION = State()
    GET_REPORT = State()
