import re
import json
import threading
from md2tgmd import escape

from secret import COOKIES
from telegram.constants import ChatAction
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle


class AIBot:
    def __init__(self):
        self.cookiesBing = COOKIES
        self.conversationStyle = ConversationStyle.balanced

        if self.cookiesBing:
            try:
                print(json.loads(self.cookiesBing))
                # self.botBing = Chatbot(cookies=json.loads(self.cookiesBing))
                f = open('bing_cookies_*.json')
                cookie_current=json.load(f)
                f.close()
                print(cookie_current)
                self.botBing = Chatbot(cookies=cookie_current)
            except Exception as e:
                print("\033[31m")
                print("Please check cookies!")
                print("error", e)
                print("\033[0m")
                self.cookiesBing = None

    async def getBing(self, message, update, context):
        result = "Something went wrong."
        try:
            result = await self.botBing.ask(
                prompt=message, conversation_style=self.conversationStyle
            )
            numMessages = result["item"]["throttling"]["numUserMessagesInConversation"]
            maxNumMessages = result["item"]["throttling"][
                "maxNumUserMessagesInConversation"
            ]

            result = result["item"]["messages"][1]["text"]
            if numMessages == maxNumMessages:
                await self.botBing.reset()
        except Exception as e:
            print("\033[31m")
            print("response_msg", result)
            print("error", e)
            print("\033[0m")
            numMessages = 0
            maxNumMessages = 0
            result = "Something went wrong."
            await self.botBing.reset()
        result = re.sub(r"\[\^\d+\^\]", "", result)
        toSend = f"{result} ({numMessages}/{maxNumMessages})"
        print(toSend)
        with open("log.txt", "a") as log:
            log.write(toSend)

        message = await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=escape(toSend),
            parse_mode="MarkdownV2",
            reply_to_message_id=update.message.message_id,
        )

    async def getResult(self, update, context):
        print(
            "\033[32m",
            update.effective_user.id,
            update.message.text,
            "\033[0m",
        )

        # with open("log.txt", "a") as log:
        #     log.write(f"\n{update.effective_user.id}:{update.message.text}\n")
        chat_content = update.message.text
        if self.cookiesBing and chat_content:
            await self.getBing(chat_content, update, context)

    async def reset_chat(self, update, context):
        await self.botBing.reset()
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Reset ✓",
        )

    async def reset_creative(self, update, context):
        await self.reset_chat(update, context)
        self.conversationStyle = ConversationStyle.creative

    async def reset_balanced(self, update, context):
        await self.reset_chat(update, context)
        self.conversationStyle = ConversationStyle.balanced

    async def reset_precise(self, update, context):
        await self.reset_chat(update, context)
        self.conversationStyle = ConversationStyle.precise
