from aiogram import types
from data.database import usage, error
from aiogram.types import Message


async def process_message(message: Message):
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "None"
    chat_id = message.chat.id

    response = f"*Your user ID:* `{user_id}`\n*Current chat ID:* `{chat_id}`"

    # Check if message has been forwarded
    if message.forward_from:
        forward_id = message.forward_from.id
        forward_username = f"@{message.forward_from.username}" if message.forward_from.username else "None"
        response += f"\n*Forwarded from:* `{forward_id}` || {forward_username}"

    elif message.forward_from_chat:
        forward_chat_id = message.forward_from_chat.id
        forward_chat_username = f"@{message.forward_from_chat.username}" if message.forward_from_chat.username else "None"
        response += f"\n*Forwarded from:* `{forward_chat_id}` || {forward_chat_username}"

    # # Check if a message is forwarded from a channel or chat
    # if message.forward_from_message_id:
    #     forward_id = message.forward_from_message_id
    #     response += f"\n\n*Forwarded message ID:* `{forward_id}`"

    usage(user_id)

    try:
        await message.reply(response, parse_mode="Markdown")
    except Exception as e:
        # Error logging (if needed)
        error(user_id, username, str(e))
        await message.reply("An error occurred while processing your message.")
