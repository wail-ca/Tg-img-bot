import time
import uuid
from PIL import Image, ImageDraw, ImageFont
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_filters
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.asyncio_storage import StateMemoryStorage

# Add your bot token here
API_TOKEN = "BOT_TOKEN"
bot = AsyncTeleBot(API_TOKEN)

# Configuration
font_size = 155
font_color = (200, 200, 200)

# Bot state storage and filter setup
state_storage = StateMemoryStorage()
bot.add_custom_filter(asyncio_filters.StateFilter(bot))


class MyStates(StatesGroup):
    name = State()


# Start command handler
@bot.message_handler(commands=["start"])
async def start(message):
    chat_id = message.chat.id
    await bot.reply_to(message, f"ℹ️ Enter a name...")
    await bot.set_state(chat_id, MyStates.name, chat_id)


@bot.message_handler(state=MyStates.name)
async def put_name(message):
    text = message.text
    text = text.replace(" ", "\n")
    fileName = uuid.uuid4()

    # Picking the image needed
    im = Image.open("design.png")
    draw = ImageDraw.Draw(im)
    unicode_font = ImageFont.truetype("cairo.ttf", font_size)

    # Drawing the text configs
    draw.text(
        (40, 260),
        text,
        font=unicode_font,
        fill=font_color,
        stroke_width=0
    )
    # Saving the image
    im.save(f"gens/{fileName}.png")

    # Sending it to the user
    await bot.send_photo(message.chat.id, open(f"gens/{fileName}.png", "rb"))


async def main():
    polling_task = asyncio.create_task(bot.infinity_polling())
    await asyncio.gather(
        polling_task,
    )


if __name__ == "__main__":
    asyncio.run(main())
