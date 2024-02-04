from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards.basic import AnswersKeyboard, ReportKeyboard
from core.settings import QUESTIONS
from core.utils.stateforms import ReportForm, ReportQuestionForm


async def questions_initiate_state(location: str, state: FSMContext):
    await state.set_data(
        {
            "location": location,
            "question_number": 1,
            "questions_len": len(QUESTIONS),
        }
    )


async def question_ask(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(ReportQuestionForm.GET_ANSWER)
    await message.answer(
        QUESTIONS[data["question_number"] - 1],
        reply_markup=AnswersKeyboard.get_keyboard(),
    )


async def questions_are_ended(state: FSMContext) -> bool:
    data = await state.get_data()
    if data["question_number"] == data["questions_len"]:
        return True
    return False


async def set_next_question(state: FSMContext):
    data = await state.get_data()
    await state.update_data({
        "question_number": data["question_number"] + 1
    })
    await state.set_state(ReportQuestionForm.GET_ANSWER)


async def process_report(message: Message):
    await message.answer(
        "Звіт сформований. Ви можете його переглянути або одразу надіслати. "
        "Для цього натисність відповідну кнопку.",
        reply_markup=ReportKeyboard.get_keyboard()
    )


async def process_question_end(message: Message, state: FSMContext):
    ended = await questions_are_ended(state)

    if not ended:
        await set_next_question(state)
        await question_ask(message, state)

    else:
        await state.set_state(ReportForm.GET_REPORT)
        await process_report(message)
