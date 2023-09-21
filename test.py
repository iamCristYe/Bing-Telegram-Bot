import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

#from secret import COOKIES

async def main():
    bot = await Chatbot.create() # Passing cookies is "optional", as explained above
    response = await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative, simplify_response=True)
    print(json.dumps(response, indent=2)) # Returns
    """
{
    "text": str,
    "author": str,
    "sources": list[dict],
    "sources_text": str,
    "suggestions": list[str],
    "messages_left": int
}
    """
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())