from aiogram import Bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from OpenAI.prompts import get_location_report_prompt
from OpenAI.utils import get_analysis_from_ai
from core.keyboards.basic import (
    start_keyboard, get_locations_keyboard,
    AnswersKeyboard, SkipPictureKeyboard, ReportKeyboard
)
from core.settings import LOCATIONS, QUESTIONS, TELEGRAM_FILE_STORAGE_URL
from core.utils.report_states import questions_initiate_state, question_ask, process_question_end
from core.utils.stateforms import ReportForm, ReportQuestionForm

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    answer = "Ласкаво просимо! Ви викликали команду /start.\n"
    answer += "Тепер викличте команду /report для відправлення звіту."
    await message.answer(answer, reply_markup=start_keyboard)


@router.message(Command("report"))
async def cmd_report(message: Message, state: FSMContext) -> None:
    await message.answer("Викликали команду /report. Тут ви можете розповісти про щось або відправити фото.")
    await message.answer(
        "Оберіть місто:",
        reply_markup=get_locations_keyboard(LOCATIONS)
    )
    await state.set_state(ReportForm.GET_LOCATION)


@router.message(ReportForm.GET_LOCATION, F.text.in_(LOCATIONS))
async def select_location(message: Message, state: FSMContext):
    await questions_initiate_state(message.text, state)
    await question_ask(message, state)


@router.message(ReportQuestionForm.GET_ANSWER, F.text)
async def process_answer(message: Message, state: FSMContext):
    if message.text == AnswersKeyboard.answer_ok:
        data = await state.get_data()
        question_tag = f"Q{data['question_number']}"
        await state.update_data({
            question_tag: {
                "question": QUESTIONS[data["question_number"] - 1],
                "comment": AnswersKeyboard.answer_ok,
                "image": None,
            }
        })

        await process_question_end(message, state)

    elif message.text == AnswersKeyboard.answer_comment:
        await state.set_state(ReportQuestionForm.GET_COMMENT)
        await message.answer("Напишіть ваш коментар")

    else:
        await message.answer("Я не зрозумів Вас. Будь ласка, оберіть один з двох варіантів")
        await question_ask(message, state)


@router.message(ReportQuestionForm.GET_COMMENT, F.text)
async def process_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    question_tag = f"Q{data['question_number']}"
    await state.update_data({
        question_tag: {
            "question": QUESTIONS[data["question_number"] - 1],
            "comment": message.text,
            "image": None,
        }
    })

    await state.set_state(ReportQuestionForm.GET_PICTURE)
    await message.answer(
        'Ваш коментар було збережено. Можете надіслати зображення до вашого коментаря. '
        'Ви можете пропустити цей етап, натиснувши кнопку "Далі", або відправивши інше повідомлення.',
        reply_markup=SkipPictureKeyboard.get_keyboard()
    )


@router.message(ReportQuestionForm.GET_PICTURE, F.photo)
async def process_photo(message: Message, state: FSMContext, bot: Bot):
    file = await bot.get_file(message.photo[-1].file_id)
    file_url = TELEGRAM_FILE_STORAGE_URL + file.file_path

    data = await state.get_data()
    question_tag = f"Q{data['question_number']}"
    data[question_tag].update({
        "image": file_url,
    })
    question_tag = f"Q{data['question_number']}"

    await state.update_data({question_tag: data[question_tag]})

    await message.answer(f"Зображення завантажено. Перейдемо до наступного питання.")
    await process_question_end(message, state)


@router.message(ReportQuestionForm.GET_PICTURE, F.text)
async def process_photo_skip(message: Message, state: FSMContext):
    await process_question_end(message, state)


@router.message(ReportForm.GET_REPORT, F.text == ReportKeyboard.report_view)
async def process_photo_skip(message: Message, state: FSMContext):
    data = await state.get_data()

    report = f"Локація: {data['location']}"

    for i in range(1, len(QUESTIONS) + 1):
        question_tag = f"Q{i}"
        report += f"\n\n<b>Питання {i}:</b>\n{data[question_tag]['question']}"
        report += f"\n<b>Відповідь:</b> {data[question_tag]['comment']}"

        if data[question_tag]['image']:
            report += "\n<i>Додано зображення</i>"

    await message.answer(report, reply_markup=ReportKeyboard.get_keyboard())


@router.message(ReportForm.GET_REPORT, F.text == ReportKeyboard.report_send)
async def process_photo_skip(message: Message, state: FSMContext):
    data = await state.get_data()

    report = f"Локація: {data['location']}"

    for i in range(1, len(QUESTIONS) + 1):
        question_tag = f"Q{i}"
        report += f"\n\n<b>Питання {i}:</b>\n{data[question_tag]['question']}"
        report += f"\n<b>Відповідь:</b> {data[question_tag]['comment']}"

        if data[question_tag]['image']:
            report += f"\n<i>URL зображення: {data[question_tag]['image']}</i>"

    await message.answer("Оброблюємо запит. Почекайте будь ласка.")
    await state.clear()

    report = get_location_report_prompt(report)
    report = await get_analysis_from_ai(report)
    report = "Вам бажано прислухатися наступних порад:\n" + str(report)
    await message.answer(report)

    await message.answer(
        "Використовуйте команду /report для формування нового звіту.",
        reply_markup=start_keyboard
    )

