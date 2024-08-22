import os
from aiogram import types
from bot.utils import extract_file_id
from bot.message_handlers import process_message
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from cfg import DEV, CHANNEL, ADMIN_ID, GIF_1, GIF_2, GIF_3, TON, COFFEE
from data.database import add_user, usage, error, statistics, errors_count


async def start(message: types.Message):
    # add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
    #          message.from_user.last_name)
    # image_path = os.path.abspath('assets/img.png')
    # start_image = InputFile(image_path)

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="👨‍💻 DEV", url=DEV),
        InlineKeyboardButton(text="🔗 Channel", url=CHANNEL)
    )

    caption = (
        "👾 This bot will help you get Telegram sticker or GIF ID, just send it to me!\n\n"
        "🤖 Source: [GitHub Repository](https://github.com/bohd4nx/mediaID)\n\n"
        "*Available Commands:*\n"
        "/start - Start bot.\n"
        # "/about - Learn more about me.\n"
        "/help - Find out how it works.\n"
        "/donate - Support me.\n"
    )

    await message.answer_animation(
        animation=GIF_1,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=markup
    )


async def help(message: Message):
    # image_path = os.path.abspath('assets/instruction.png')
    # instruction_image = InputFile(image_path)э

    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("👨‍💻 DEV", url=DEV)
    )

    caption = (
        "ℹ️ *How to use the Bot:*\n\n"
        "1. Send me any sticker (including animated), GIF, or document.\n"
        "2. I will reply with the `<file_type>` ID.\n\n"
        "If you have any problems or suggestions, please use the button below to contact DEV."
    )

    await message.answer_animation(
        animation=GIF_2,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=markup
    )


async def donate(message: Message):
    # image_path = os.path.abspath('assets/donate.png')
    # donate_image = InputFile(image_path)

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="☕ Buy Me a Coffee", url=COFFEE),
        InlineKeyboardButton(text="💎 TON", url=TON)
    )

    caption = "🙏 *Support by donation*\n\nYour support inspires me to do more!"

    await message.answer_animation(
        animation=GIF_3,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=markup
    )


async def media(message: Message):
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "None"
    first_name = message.from_user.first_name or "Null"
    last_name = message.from_user.last_name or "Null"

    # Add user to database if not exists
    add_user(user_id, username, first_name, last_name)

    file_id = extract_file_id(message)

    media_type = (
        "Sticker" if message.sticker else
        "GIF" if message.animation else
        "Document" if message.document else
        None
    )

    if file_id:
        response = (f"*Your user ID:* `{user_id}`\n"
                    f"*{media_type} ID:* `{file_id}`"
                    )
        if media_type == "Sticker" and message.sticker:
            sticker_set_name = message.sticker.set_name
            if sticker_set_name:
                sticker_set_url = f"https://t.me/addstickers/{sticker_set_name}"
                response += f"\n\n*Add stickers:* {sticker_set_url}"

            usage(user_id)

    elif message.text or message.forward_from or message.forward_from_chat:
        await process_message(message)
        return
    else:
        response = "Unable to get ID, please dm DEV"

        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("👨‍💻 DEV", url=DEV)
        )

        await message.reply(response, reply_markup=markup)
        return

    await message.reply(response, disable_web_page_preview=True, parse_mode="Markdown")


async def db(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        total_users, total_usage = statistics()
        error_count = errors_count()
        await message.reply(f"👥 Total users: *{total_users}*\n"
                            f"👾 Total bot usages: *{total_usage}*\n"
                            f"❌ Total error logs: *{error_count}*\n"
                            f"🗃️ For more info, check: `data/database.db`",
                            parse_mode='Markdown')
    else:
        await message.reply("⛔️ Access denied.")
