import asyncio
from aiogram import F
from bot.loader import bot, dp
from bot.logging_conf import setup_logging
from bot.middlewares.admin_gate import AdminGateMiddleware
from bot.handlers.basic import router as basic_router
from bot.handlers.ai_router import router as ai_router
from bot.handlers.admin_commands import router as admin_router

async def on_startup():
    setup_logging()

def setup_middlewares():
    dp.message.middleware(AdminGateMiddleware())

def setup_routers():
    dp.include_router(basic_router)
    dp.include_router(ai_router)
    dp.include_router(admin_router)

async def main():
    await on_startup()
    setup_middlewares()
    setup_routers()
    allowed = dp.resolve_used_update_types()
    await dp.start_polling(bot, allowed_updates=allowed)

if __name__ == "__main__":
    asyncio.run(main())
