from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from utils import get_user_link

router = Router()


class MessageStates(StatesGroup):
	send = State()


@router.message(CommandStart())
async def start(message: Message, bot: Bot, state: FSMContext):
	args = message.text.split()[1:]
	if len(args) > 0:
		id = int(args[0], 16)
		await send_anon(message.from_user.id, id, bot, state)
	else:
		await bot.send_message(message.from_user.id, '<b>Начните получать анонимные вопросы прямо сейчас!</b>\n\n'
													 f'👉 t.me/anonimnyy_voprosy_bot?start={get_user_link(message.from_user.id)}\n\n'
													 '<b>Разместите эту ссылку</b> ☝️ в описании своего профиля Telegram, TikTok, Instagram (stories), <b>чтобы вам могли написать</b> 💬',
							   reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
								   text='🔗 Поделиться ссылкой', url='t.me/anonimnyye_voprosy_bot?start')]]))


async def send_anon(user_id: int, to_user: int, bot: Bot, state: FSMContext):
	msg = await bot.send_message(user_id,
								 '🚀 Здесь можно отправить <b>анонимное сообщение</b> человеку, который опубликовал эту ссылку\n\n'
								 '🖊 <b>Напишите сюда всё, что хотите ему передать,</b> и через несколько секунд он получит ваше сообщение, но не будет знать от кого\n\n'
								 'Отправить можно фото, видео, 💬 текст, 🔊 голосовые, 📷 видеосообщения (кружки), а также ✨ стикеры',
								 reply_markup=InlineKeyboardMarkup(
									 inline_keyboard=[
										 [InlineKeyboardButton(text='✖️ Отменить', callback_data='cancel')]]))
	await state.set_state(MessageStates.send)
	await state.set_data({'user_id': to_user, 'message': msg})


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
	await callback.message.delete()
	await callback.answer()
	await state.clear()


@router.message(MessageStates.send)
async def send_state(message: Message, bot: Bot, state: FSMContext):
	await (await state.get_value('message')).delete()
	user_id = await state.get_value('user_id')
	await state.clear()
	await bot.send_message(message.from_user.id, 'Сообщение отправлено, ожидайте ответ!',
						   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
							   [InlineKeyboardButton(text='Написать еще ✍️', callback_data=f'send;{user_id}')]]))
	try:
		await bot.send_message(user_id,
							   f'{message.from_user.full_name} (@{message.from_user.username}) отправил тебе сообщение:\n\n'
							   f'{message.text}')
	except:
		pass


@router.callback_query(F.data.split(';')[0] == 'send')
async def send_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
	await send_anon(callback.from_user.id, int(callback.data.split(';')[1]), bot, state)
	await callback.answer()
