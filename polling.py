import telegram
import threading
from bot import setup
from urllib import parse
from waitress import serve
from runasync import run_async
from flask import Flask, request, jsonify
from config import BOT_TOKEN
from telegram.ext import filters, MessageHandler

application = setup(BOT_TOKEN)


# def hello():
#     print("", end="")
#     return "Bot has connected!"


# async def respond():
#     update = telegram.Update.de_json(request.get_json(force=True), application.bot)
#     run_async(application.initialize())
#     thread = threading.Thread(
#         target=run_async, args=(application.process_update(update),)
#     )
#     thread.start()
#     return jsonify({"status": "success", "message": "Received message successfully."})


# async def configure_webhook():
#     webhookUrl = parse.urljoin(WEB_HOOK, rf"/{BOT_TOKEN}")
#     result = await application.bot.setWebhook(webhookUrl)
#     if result:
#         print(rf"webhook configured: {webhookUrl}")
#         return rf"webhook configured: {webhookUrl}"
#     else:
#         print("webhook setup failed")
#         return "webhook setup failed"


if __name__ == "__main__":
    # run_async(configure_webhook())
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), respond)

    # application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    # update = telegram.Update.de_json(request.get_json(force=True), application.bot)
    run_async(application.initialize())
    # application.process_update(update)

    application.run_polling()
