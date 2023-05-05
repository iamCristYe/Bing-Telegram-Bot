import logging
from md2tgmd import escape
from runasync import run_async
from telegram import BotCommand
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, filters
from AI import AIBot

ai_bot = AIBot()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# In all other places characters
# _ * [ ] ( ) ~ ` > # + - = | { } . !
# must be escaped with the preceding character '\'.
async def start(update, context):  # 当用户输入/start时，返回文本
    user = update.effective_user
    message = "Hi"
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Ask me for Bing.",
    )
    # await update.message.reply_text(escape(message), parse_mode='MarkdownV2')


async def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    await context.bot.send_message(
        chat_id=update.message.chat_id, text="出错啦！请重试。", parse_mode="MarkdownV2"
    )


async def unknown(update, context):  # 当用户输入未知命令时，返回文本
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


def setup(token):
    application = ApplicationBuilder().token(token).build()

    run_async(
        application.bot.set_my_commands(
            [
                BotCommand("start", "Start the bot"),
                BotCommand("reset", "Reset the bot"),
                BotCommand("reset-creative", "Reset to creative style"),
                BotCommand("reset-balanced", "Reset to balanced style"),
                BotCommand("reset-precise", "Reset to precise style"),
            ]
        )
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", ai_bot.reset_chat))

    application.add_handler(MessageHandler(filters.TEXT, ai_bot.getResult))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(error)

    return application
