from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from globals import CAN_SEE_USERS

router = Router()


class MessageStates(StatesGroup):
    send = State()


async def send_to(user_id: int, target_id: int, bot: Bot, state: FSMContext):
    msg = await bot.send_message(user_id,
                                 '🚀 Здесь можно отправить <b>анонимное сообщение</b> человеку, который опубликовал эту ссылку\n\n'
                                 '🖊 <b>Напишите сюда всё, что хотите ему передать,</b> и через несколько секунд он получит ваше сообщение, но не будет знать от кого\n\n'
                                 'Отправить можно фото, видео, 💬 текст, 🔊 голосовые, 📷 видеосообщения (кружки), а также ✨ стикеры',
                                 reply_markup=InlineKeyboardMarkup(
                                     inline_keyboard=[
                                         [InlineKeyboardButton(text='✖️ Отменить', callback_data='cancel')]]))
    await state.set_state(MessageStates.send)
    await state.set_data({'user_id': target_id, 'message': msg})


@router.message(MessageStates.send)
async def send_state(message: Message, bot: Bot, state: FSMContext):
    await (await state.get_value('message')).delete()
    user_id = await state.get_value('user_id')
    await state.clear()
    await bot.send_message(message.from_user.id, 'Сообщение отправлено, ожидайте ответ!',
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                               [InlineKeyboardButton(text='Написать еще ✍️', callback_data=f'send;{user_id}')]]))

    text = '🔔 <b>У тебя новое сообщение!</b>\n\n'
    if message.text:
        text += f'<blockquote>{message.text}</blockquote>\n\n'
    text += '↩️ <i>Свайпни для ответа.</i>'

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🚮 Пожаловаться', callback_data='report')]])

    if user_id in CAN_SEE_USERS:
        text += f'\n\nОт {message.from_user.full_name}'
        if message.from_user.username:
            text += f' (@{message.from_user.username})'
        keyboard.inline_keyboard += [[InlineKeyboardButton(text='Открыть профиль',
                                                           url=f'tg://user?id={message.from_user.id}')]]

    try:
        await bot.send_message(user_id, text, reply_markup=keyboard)
    except:
        pass


@router.callback_query(F.data.split(';')[0] == 'send')
async def send_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await send_to(callback.from_user.id, int(callback.data.split(';')[1]), bot, state)
    await callback.answer()
