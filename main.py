from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, UpdateType

from handlers import message, anonimous_sending


async def main():
    bot = Bot('8016428741:AAGrfQfukD-tR-Veg7M9Sv0_wGf1HUGJkhU',
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dispatcher = Dispatcher()

    dispatcher.include_routers(anonimous_sending.router,
                               message.router)

    await dispatcher.start_polling(bot,
                                   allowed_updates=[UpdateType.MESSAGE,
                                                    UpdateType.CALLBACK_QUERY],
                                   polling_timeout=30)


if __name__ == '__main__':
    run(main())
