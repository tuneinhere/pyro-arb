from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, 
                            ReplyKeyboardRemove, KeyboardButton, ForceReply)
from typing import List, Union

# --- KELAS TOMBOL (WRAPPERS) ---

class InlineButton(InlineKeyboardButton):
    """Jembatan untuk Inline Button agar support Style"""
    def __init__(self, text=None, callback_data=None, url=None, style=None, **kwargs):
        super().__init__(text=text, callback_data=callback_data, url=url, style=style, **kwargs)

class ReplyButton(KeyboardButton):
    """Jembatan untuk Reply Button agar support Style"""
    def __init__(self, text=None, request_contact=None, request_location=None, style=None, **kwargs):
        super().__init__(text=text, request_contact=request_contact, request_location=request_location, style=style, **kwargs)

# --- KELAS KEYBOARD (LAYOUTERS) ---

class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, row_width=3):
        self.inline_keyboard = list()
        super().__init__(inline_keyboard=self.inline_keyboard)
        self.row_width = row_width

    def add(self, *args):
        processed_btns = []
        for btn in args:
            if isinstance(btn, (list, tuple)):
                # Memproses format ["Teks", "Data", Style]
                text = btn[0]
                val = btn[1]
                style = btn[2] if len(btn) > 2 else None
                if isinstance(val, str) and val.startswith("http"):
                    processed_btns.append(InlineButton(text=text, url=val, style=style))
                else:
                    processed_btns.append(InlineButton(text=text, callback_data=str(val), style=style))
            else:
                processed_btns.append(btn)
        
        self.inline_keyboard = [processed_btns[i:i + self.row_width] for i in range(0, len(processed_btns), self.row_width)]

class ReplyKeyboard(ReplyKeyboardMarkup):
    def __init__(self, resize_keyboard=True, one_time_keyboard=None, selective=None, placeholder=None, row_width=3):
        self.keyboard = list()
        super().__init__(keyboard=self.keyboard, resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard, selective=selective, placeholder=placeholder)
        self.row_width = row_width

    def add(self, *args):
        processed_btns = []
        for btn in args:
            if isinstance(btn, (list, tuple)):
                # Memproses format ["Teks", Style]
                processed_btns.append(ReplyButton(text=btn[0], style=btn[1] if len(btn) > 1 else None))
            else:
                processed_btns.append(btn)
        self.keyboard = [processed_btns[i:i + self.row_width] for i in range(0, len(processed_btns), self.row_width)]

# --- KELAS TAMBAHAN ---

class ReplyKeyboardRemove(ReplyKeyboardRemove):
    def __init__(self, selective=None): super().__init__(selective=selective)

class ForceReply(ForceReply):
    def __init__(self, selective=None, placeholder=None): super().__init__(selective=selective, placeholder=placeholder)
