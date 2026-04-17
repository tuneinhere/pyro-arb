from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ForceReply,
)

# Optional enum
try:
    from pyrogram.enums import ButtonStyle
except:
    ButtonStyle = None


def btn(text, value=None, type="callback_data", style=None, **extra):
    """
    Extended InlineKeyboardButton

    Supports:
    - (text, value)
    - (text, value, type)
    - (text, value, type, style)
    - kwargs tambahan (misal: url, dll)
    """

    kwargs = {}

    if value:
        kwargs[type] = value

    if style is not None:
        kwargs["style"] = style  # ✅ langsung kirim ke Pyrogram mod lu

    kwargs.update(extra)

    return InlineKeyboardButton(text, **kwargs)


def ikb(rows=None):
    """
    Flexible InlineKeyboard builder
    """
    if rows is None:
        rows = []

    lines = []
    for row in rows:
        line = []

        for button in row:
            # ========================
            # STRING
            # ========================
            if isinstance(button, str):
                line.append(btn(button, button))

            # ========================
            # TUPLE / LIST
            # ========================
            elif isinstance(button, (list, tuple)):
                l = len(button)

                if l == 4:
                    text, value, type, style = button
                    line.append(btn(text, value, type, style))

                elif l == 3:
                    text, value, third = button

                    # 🔥 AUTO DETECT
                    if isinstance(third, str) and third in [
                        "callback_data",
                        "url",
                        "switch_inline_query",
                        "switch_inline_query_current_chat",
                        "callback_game",
                    ]:
                        line.append(btn(text, value, third))
                    else:
                        # anggap style
                        line.append(btn(text, value, "callback_data", third))

                elif l == 2:
                    text, value = button
                    line.append(btn(text, value))

                else:
                    raise ValueError(f"Invalid button format: {button}")

            # ========================
            # LANGSUNG BUTTON OBJECT
            # ========================
            elif isinstance(button, InlineKeyboardButton):
                line.append(button)

            else:
                raise TypeError(f"Unsupported button type: {type(button)}")

        lines.append(line)

    return InlineKeyboardMarkup(inline_keyboard=lines)


# =============================
# REVERSE (UPDATED SUPPORT STYLE)
# =============================

def bki(keyboard):
    lines = []
    for row in keyboard.inline_keyboard:
        line = []
        for button in row:
            line.append(ntb(button))
        lines.append(line)
    return lines


def ntb(button):
    btn_type = None
    value = None

    for t in [
        "callback_data",
        "url",
        "switch_inline_query",
        "switch_inline_query_current_chat",
        "callback_game",
    ]:
        v = getattr(button, t, None)
        if v:
            btn_type = t
            value = v
            break

    result = [button.text, value]

    if btn_type and btn_type != "callback_data":
        result.append(btn_type)

    # ✅ TAMBAHAN: ambil style kalau ada
    style = getattr(button, "style", None)
    if style is not None:
        if btn_type and btn_type != "callback_data":
            result.append(style)
        else:
            result.append(style)

    return result


# =============================
# REPLY KEYBOARD (UNCHANGED)
# =============================

def kb(rows=None, **kwargs):
    if rows is None:
        rows = []

    lines = []
    for row in rows:
        line = []
        for button in row:
            if isinstance(button, str):
                button = KeyboardButton(button)
            elif isinstance(button, dict):
                button = KeyboardButton(**button)

            line.append(button)
        lines.append(line)

    return ReplyKeyboardMarkup(keyboard=lines, **kwargs)


kbtn = KeyboardButton


def force_reply(selective=True):
    return ForceReply(selective=selective)


def array_chunk(input_array, size):
    return [input_array[i: i + size] for i in range(0, len(input_array), size)]