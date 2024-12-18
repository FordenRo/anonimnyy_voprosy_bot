from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from handlers.anonimous_sending import send_to
from utils import get_user_link

router = Router()


async def send_start_message(user_id: int, bot: Bot):
    await bot.send_message(user_id, '<b>Начните получать анонимные вопросы прямо сейчас!</b>\n\n'
                                    f'👉 t.me/anonimnyy_voprosy_bot?start={get_user_link(user_id)}\n\n'
                                    '<b>Разместите эту ссылку</b> ☝️ в описании своего профиля Telegram, TikTok, Instagram (stories), <b>чтобы вам могли написать</b> 💬',
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                               text='🔗 Поделиться ссылкой', url='t.me/anonimnyye_voprosy_bot?start')]]))


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()
    await state.clear()


@router.message()
async def message(message: Message, bot: Bot, state: FSMContext):
    if message.text.startswith('/start'):
        args = message.text.split()
        if len(args) > 1:
            target_id = int(args[1], 16)
            await send_to(message.from_user.id, target_id, bot, state)
            return

    await send_start_message(message.from_user.id, bot)
