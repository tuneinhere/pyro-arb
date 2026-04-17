from pyrogram.emoji import (FLAG_UKRAINE, FLAG_UZBEKISTAN, FLAG_SPAIN, FLAG_TURKEY, 
                            FLAG_BELARUS, FLAG_GERMANY, FLAG_CHINA, FLAG_UNITED_KINGDOM, 
                            FLAG_FRANCE, FLAG_INDONESIA, FLAG_ITALY, FLAG_SOUTH_KOREA, FLAG_RUSSIA)
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, 
                            ReplyKeyboardRemove, KeyboardButton, ForceReply)
from typing import List, Union

class InlineButton(InlineKeyboardButton):
    def __init__(self, text=None, callback_data=None, url=None,
                 login_url=None, user_id=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, callback_game=None, style=None):
        super().__init__(
            text=text,
            callback_data=callback_data,
            url=url,
            login_url=login_url,
            user_id=user_id,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            callback_game=callback_game,
            style=style
        )

class InlineKeyboard(InlineKeyboardMarkup):
    _SYMBOL_FIRST_PAGE = '« {}'
    _SYMBOL_PREVIOUS_PAGE = '‹ {}'
    _SYMBOL_CURRENT_PAGE = '· {} ·'
    _SYMBOL_NEXT_PAGE = '{} ›'
    _SYMBOL_LAST_PAGE = '{} »'
    _LOCALES = {
        'be_BY': f'{FLAG_BELARUS} Беларуская',
        'de_DE': f'{FLAG_GERMANY} Deutsch',
        'zh_CN': f'{FLAG_CHINA} 中文',
        'en_US': f'{FLAG_UNITED_KINGDOM} English',
        'fr_FR': f'{FLAG_FRANCE} Français',
        'id_ID': f'{FLAG_INDONESIA} Bahasa Indonesia',
        'it_IT': f'{FLAG_ITALY} Italiano',
        'ko_KR': f'{FLAG_SOUTH_KOREA} 한국어',
        'tr_TR': f'{FLAG_TURKEY} Türkçe',
        'ru_RU': f'{FLAG_RUSSIA} Русский',
        'es_ES': f'{FLAG_SPAIN} Español',
        'uk_UA': f'{FLAG_UKRAINE} Українська',
        'uz_UZ': f'{FLAG_UZBEKISTAN} Oʻzbekcha',
    }

    def __init__(self, row_width=3):
        self.inline_keyboard = list()
        super().__init__(inline_keyboard=self.inline_keyboard)
        self.row_width = row_width

    def add(self, *args):
        processed_btns = []
        for btn in args:
            if isinstance(btn, (list, tuple)):
                processed_btns.append(self._parse_btn(btn))
            else:
                processed_btns.append(btn)
        self.inline_keyboard = [
            processed_btns[i:i + self.row_width]
            for i in range(0, len(processed_btns), self.row_width)
        ]

    def row(self, *args):
        processed_btns = []
        for btn in args:
            if isinstance(btn, (list, tuple)):
                processed_btns.append(self._parse_btn(btn))
            else:
                processed_btns.append(btn)
        self.inline_keyboard.append(processed_btns)

    def _parse_btn(self, btn_data):
        text = btn_data[0]
        value = btn_data[1]
        style = btn_data[2] if len(btn_data) > 2 else None
        if isinstance(value, str) and value.startswith("http"):
            return InlineButton(text=text, url=value, style=style)
        return InlineButton(text=text, callback_data=str(value), style=style)

class InlinePaginationKeyboard(InlineKeyboardMarkup):
    SYMBOL_FIRST_PAGE = '« {}'
    SYMBOL_PREVIOUS_PAGE = '‹ {}'
    SYMBOL_CURRENT_PAGE = '· {} ·'
    SYMBOL_NEXT_PAGE = '{} ›'
    SYMBOL_LAST_PAGE = '{} »'

    def __init__(self, count_pages: int, current_page: int, callback_pattern: str, style=None):
        self.inline_keyboard = list()
        super().__init__(inline_keyboard=self.inline_keyboard)
        self.count_pages = count_pages
        self.current_page = current_page
        self.callback_pattern = callback_pattern
        self.style = style
        self._build()

    def add_button(self, text, callback_data):
        return InlineButton(
            text=str(text),
            callback_data=self.callback_pattern.format(number=callback_data),
            style=self.style
        )

    def _build(self):
        # Sederhananya kita pakai full pagination dulu agar kurung aman
        btns = []
        for n in range(1, self.count_pages + 1):
            txt = self.SYMBOL_CURRENT_PAGE.format(n) if n == self.current_page else n
            btns.append(self.add_button(txt, n))
        self.inline_keyboard.append(btns)

class ReplyButton(KeyboardButton):
    def __init__(self, text=None, request_contact=None, request_location=None, style=None):
        super().__init__(text=text, request_contact=request_contact, request_location=request_location, style=style)

class ReplyKeyboard(ReplyKeyboardMarkup):
    def __init__(self, resize_keyboard=True, one_time_keyboard=None, selective=None, placeholder=None, row_width=3):
        self.keyboard = list()
        super().__init__(keyboard=self.keyboard, resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard, selective=selective, placeholder=placeholder)
        self.row_width = row_width

    def add(self, *args):
        processed = []
        for btn in args:
            if isinstance(btn, (list, tuple)):
                processed.append(ReplyButton(text=btn[0], style=btn[1] if len(btn) > 1 else None))
            else:
                processed.append(btn)
        self.keyboard = [processed[i:i + self.row_width] for i in range(0, len(processed), self.row_width)]

    def row(self, *args):
        self.keyboard.append([ReplyButton(text=b[0], style=b[1] if len(b)>1 else None) if isinstance(b, (list, tuple)) else b for b in args])

class ReplyKeyboardRemove(ReplyKeyboardRemove):
    def __init__(self, selective=None):
        super().__init__(selective=selective)

class ForceReply(ForceReply):
    def __init__(self, selective=None, placeholder=None):
        super().__init__(selective=selective, placeholder=placeholder)
