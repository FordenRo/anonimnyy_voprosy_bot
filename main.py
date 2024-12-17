from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from handlers import start


async def main():
    bot = Bot('8016428741:AAGrfQfukD-tR-Veg7M9Sv0_wGf1HUGJkhU',
              default=DefaultBotProperties(parse_mode='html'))

    dispatcher = Dispatcher()

    dispatcher.include_routers(start.router)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    run(main())
