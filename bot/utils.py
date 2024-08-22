from aiogram import types


def extract_file_id(content: types.Message) -> str:
    if content.sticker:
        return content.sticker.file_id
    elif content.animation:
        return content.animation.file_id
    elif content.document:
        return content.document.file_id
    return None
