import telegram
import threading
from bot import setup, addHandler
from urllib import parse
from waitress import serve
from flask import Flask, request, jsonify
from secret import BOT_TOKEN
from telegram.ext import filters, MessageHandler
import asyncio


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
async def main():
    # print("done!")

    import os

    PROXY = "http://192.168.1.8:7890"

    os.environ["ALL_PROXY"] = PROXY
    os.environ["HTTP_PROXY"] = PROXY
    os.environ["HTTPS_PROXY"] = PROXY

    # run_async(configure_webhook())
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), respond)

    # application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    # update = telegram.Update.de_json(request.get_json(force=True), application.bot)
    application = setup(BOT_TOKEN)
    await addHandler(application)
    await application.initialize()
    # application.process_update(update)
    await application.run_polling()


import nest_asyncio

nest_asyncio.apply()
asyncio.run(main())
