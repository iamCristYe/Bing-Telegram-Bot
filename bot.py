import logging
from md2tgmd import escape
from telegram import BotCommand
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, filters
from AI import AIBot

ai_bot = AIBot()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


async def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


async def unknown(update, context):  # 当用户输入未知命令时，返回文本
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


def setup(token):
    application = ApplicationBuilder().token(token).build()
    return application


async def addHandler(application):
    await application.bot.set_my_commands(
        [
            BotCommand("reset_creative", "Creative style"),
            BotCommand("reset_balanced", "Balanced style"),
            BotCommand("reset_precise", "Precise style"),
        ]
    )

    application.add_handler(CommandHandler("reset_creative", ai_bot.reset_creative))
    application.add_handler(CommandHandler("reset_balanced", ai_bot.reset_balanced))
    application.add_handler(CommandHandler("reset_precise", ai_bot.reset_precise))

    application.add_handler(MessageHandler(filters.TEXT, ai_bot.getResult))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(error)
