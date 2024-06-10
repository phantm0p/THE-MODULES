# BOT/features/font.py

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import BOT.key as key

def get_font_buttons(text):
    buttons = [
        [
            InlineKeyboardButton("BOLD", callback_data=f"bold:{text}"),
            InlineKeyboardButton("ITALIC", callback_data=f"italic:{text}"),
            InlineKeyboardButton("UNDERLINE", callback_data=f"underline:{text}")
        ],
        [
            InlineKeyboardButton("SMALL CAPS", callback_data=f"small_caps:{text}"),
            InlineKeyboardButton("OUTLINE", callback_data=f"outline:{text}"),
            InlineKeyboardButton("SERIF", callback_data=f"serif:{text}")
        ],
        [
            InlineKeyboardButton("COMIC", callback_data=f"comic:{text}"),
            InlineKeyboardButton("FROZEN", callback_data=f"frozen:{text}"),
            InlineKeyboardButton("CURSIVE", callback_data=f"cursive:{text}")
        ],
        [
            InlineKeyboardButton("ARROWS", callback_data=f"arrows:{text}"),
            InlineKeyboardButton("SLASH", callback_data=f"slash:{text}"),
            InlineKeyboardButton("UPSIDEDOWN", callback_data=f"upsidedown:{text}")
        ],
        [
            InlineKeyboardButton("FRAKTUR", callback_data=f"fraktur:{text}"),
            InlineKeyboardButton("FANTASY", callback_data=f"fantasy:{text}"),
            InlineKeyboardButton("MONOSPACE", callback_data=f"monospace:{text}")
        ],
        [
            InlineKeyboardButton("FUTURA", callback_data=f"futura:{text}"),
            InlineKeyboardButton("GAARMOND", callback_data=f"gaarmond:{text}"),
            InlineKeyboardButton("FLAKY", callback_data=f"flaky:{text}")
        ],
        [
            InlineKeyboardButton("MANGA", callback_data=f"manga:{text}"),
            InlineKeyboardButton("LUNA", callback_data=f"luna:{text}"),
            InlineKeyboardButton("ZEBRA", callback_data=f"zebra:{text}")
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def apply_font(style, text):
    if style == "bold":
        return f"**{text}**"
    elif style == "italic":
        return f"__{text}__"
    elif style == "underline":
        return f"~~{text}~~"
    elif style == "small_caps":
        return key.map_text(key.small_caps, text)
    elif style == "outline":
        return key.map_text(key.outline, text)
    elif style == "serif":
        return key.map_text(key.serif, text)
    elif style == "comic":
        return key.map_text(key.comic, text)
    elif style == "frozen":
        return key.map_text(key.frozen, text)
    elif style == "arrows":
        return key.map_text(key.arrows, text)
    elif style == "slash":
        return key.map_text(key.slash, text)
    elif style == "upsidedown":
        return key.map_text(key.upsidedown, text)
    elif style == "fraktur":
        return key.map_text(key.fraktur, text)
    elif style == "fantasy":
        return key.map_text(key.fantasy, text)
    elif style == "monospace":
        return key.map_text(key.monospace, text)
    elif style == "futura":
        return key.map_text(key.futura, text)
    elif style == "gaarmond":
        return key.map_text(key.gaarmond, text)
    elif style == "flaky":
        return key.map_text(key.flaky, text)
    elif style == "manga":
        return key.map_text(key.manga, text)
    elif style == "luna":
        return key.map_text(key.luna, text)
    elif style == "zebra":
        return key.map_text(key.zebra, text)
    elif style == "cursive":
        return key.map_text(key.cursive, text)
