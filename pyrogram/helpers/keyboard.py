from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, 
                            ReplyKeyboardRemove, KeyboardButton, ForceReply)
from typing import List, Union

# --- KELAS TOMBOL ---
class InlineButton(InlineKeyboardButton):
    def __init__(self, text=None, callback_data=None, url=None, style=None, **kwargs):
        super().__init__(text=text, callback_data=callback_data, url=url, style=style, **kwargs)

class ReplyButton(KeyboardButton):
    def __init__(self, text=None, request_contact=None, request_location=None, style=None, **kwargs):
        super().__init__(text=text, request_contact=request_contact, request_location=request_location, style=style, **kwargs)

# --- KELAS KEYBOARD UTAMA ---
class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, row_width=3):
        self.inline_keyboard = list()
        super().__init__(inline_keyboard=self.inline_keyboard)
        self.row_width = row_width

    def add(self, *args):
        processed = []
        for btn in args:
            if isinstance(btn, (list, tuple)):
                text, val = btn[0], btn[1]
                style = btn[2] if len(btn) > 2 else None
                if isinstance(val, str) and val.startswith("http"):
                    processed.append(InlineButton(text=text, url=val, style=style))
                else:
                    processed.append(InlineButton(text=text, callback_data=str(val), style=style))
            else:
                processed.append(btn)
        self.inline_keyboard.extend([processed[i:i + self.row_width] for i in range(0, len(processed), self.row_width)])

# --- KELAS PAGINATION (INI YANG TADI HILANG) ---
class InlinePaginationKeyboard(InlineKeyboardMarkup):
    def __init__(self, count_pages: int, current_page: int, callback_pattern: str, style=None):
        self.inline_keyboard = list()
        super().__init__(inline_keyboard=self.inline_keyboard)
        self.count_pages = count_pages
        self.current_page = current_page
        self.callback_pattern = callback_pattern
        self.style = style
        
        # Build sederhana
        btns = []
        for n in range(1, count_pages + 1):
            txt = f"· {n} ·" if n == current_page else str(n)
            btns.append(InlineButton(text=txt, callback_data=callback_pattern.format(number=n), style=style))
        self.inline_keyboard.append(btns)

class ReplyKeyboard(ReplyKeyboardMarkup):
    def __init__(self, resize_keyboard=True, one_time_keyboard=None, selective=None, placeholder=None, row_width=3):
        self.keyboard = list()
        super().__init__(keyboard=self.keyboard, resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard, selective=selective, placeholder=placeholder)
        self.row_width = row_width

    def add(self, *args):
        processed = []
        for b in args:
            if isinstance(b, (list, tuple)):
                processed.append(ReplyButton(text=b[0], style=b[1] if len(b) > 1 else None))
            else: processed.append(b)
        self.keyboard.extend([processed[i:i + self.row_width] for i in range(0, len(processed), self.row_width)])

class ReplyKeyboardRemove(ReplyKeyboardRemove):
    def __init__(self, selective=None): super().__init__(selective=selective)

class ForceReply(ForceReply):
    def __init__(self, selective=None, placeholder=None): super().__init__(selective=selective, placeholder=placeholder)
