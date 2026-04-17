from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Union

class InlineButton(InlineKeyboardButton):
    """Wrapper agar InlineKeyboardButton mendukung parameter style"""
    def __init__(self, text, callback_data=None, url=None, style=None, **kwargs):
        super().__init__(
            text=text,
            callback_data=callback_data,
            url=url,
            style=style,
            **kwargs
        )

class InlineKeyboard(InlineKeyboardMarkup):
    _SYMBOL_FIRST_PAGE = '« {}'
    _SYMBOL_PREVIOUS_PAGE = '‹ {}'
    _SYMBOL_CURRENT_PAGE = '· {} ·'
    _SYMBOL_NEXT_PAGE = '{} ›'
    _SYMBOL_LAST_PAGE = '{} »'
    _LOCALES = {
        'be_BY': '🇧🇾 Беларуская',
        'de_DE': '🇩🇪 Deutsch',
        'zh_CN': '🇨🇳 中文',
        'en_US': '🇬🇧 English',
        'fr_FR': '🇫🇷 Français',
        'id_ID': '🇮🇩 Bahasa Indonesia',
        'it_IT': '🇮🇹 Italiano',
        'ko_KR': '🇰🇷 한국어',
        'tr_TR': '🇹🇷 Türkçe',
        'ru_RU': '🇷🇺 Русский',
        'es_ES': '🇪🇸 Español',
        'uk_UA': '🇺🇦 Українська',
        'uz_UZ': '🇺🇿 Oʻzbekcha',
    }

    def __init__(self, row_width=3):
        self.inline_keyboard = list()
        super().__init__(inline_keyboard=self.inline_keyboard)
        self.row_width = row_width

    def add(self, *args):
        """Menambahkan tombol. Bisa berupa object InlineButton atau list [text, data, style]"""
        processed_btns = []
        for btn in args:
            if isinstance(btn, (list, tuple)):
                processed_btns.append(self._parse_btn(btn))
            else:
                processed_btns.append(btn)
                
        new_rows = [
            processed_btns[i:i + self.row_width]
            for i in range(0, len(processed_btns), self.row_width)
        ]
        self.inline_keyboard.extend(new_rows)

    def row(self, *args):
        """Menambahkan satu baris tombol secara spesifik"""
        processed_btns = []
        for btn in args:
            if isinstance(btn, (list, tuple)):
                processed_btns.append(self._parse_btn(btn))
            else:
                processed_btns.append(btn)
        self.inline_keyboard.append(processed_btns)

    def _parse_btn(self, btn_data):
        """Helper internal untuk memproses format [text, data, style]"""
        text = btn_data[0]
        value = btn_data[1]
        style = btn_data[2] if len(btn_data) > 2 else 0

        if isinstance(value, str) and value.startswith("http"):
            return InlineButton(text=text, url=value, style=style)
        return InlineButton(text=text, callback_data=str(value), style=style)

    def _add_pagination_btn(self, text, callback_data, style=0):
        """Helper internal khusus untuk tombol navigasi halaman"""
        return InlineButton(
            text=str(text),
            callback_data=self.callback_pattern.format(number=callback


class InlinePaginationKeyboard(InlineKeyboardMarkup):
    SYMBOL_FIRST_PAGE = '« {}'
    SYMBOL_PREVIOUS_PAGE = '‹ {}'
    SYMBOL_CURRENT_PAGE = '· {} ·'
    SYMBOL_NEXT_PAGE = '{} ›'
    SYMBOL_LAST_PAGE = '{} »'

    def __init__(self, count_pages: int, current_page: int,
                 callback_pattern: str, style=None): # Tambahkan style opsional
        self.inline_keyboard = list()
        super().__init__(inline_keyboard=self.inline_keyboard)
        self.count_pages = count_pages
        self.current_page = current_page
        self.callback_pattern = callback_pattern
        self.style = style # Simpan style untuk digunakan di add_button
        self.markup

    def add_button(self, text, callback_data):
        # Gunakan self.style yang sudah didefinisikan saat init
        return InlineKeyboardButton(
            text=str(text),
            callback_data=self.callback_pattern.format(
                number=callback_data),
            style=self.style # Suntikkan style ke sini
        )

    # Note: Method pagination lainnya (left_pagination, build_pagination, dll) 
    # tidak perlu diubah karena mereka semua memanggil self.add_button()
    
    @property
    def left_pagination(self):
        # Otomatis menggunakan style karena memanggil add_button
        return [
            self.add_button(
                self.SYMBOL_CURRENT_PAGE.format(number), number)
            if number == self.current_page else self.add_button(
                self.SYMBOL_NEXT_PAGE.format(number), number)
            if number == 4 else self.add_button(
                self.SYMBOL_LAST_PAGE.format(self.count_pages),
                self.count_pages)
            if number == 5 else self.add_button(number, number)
            for number in range(1, 6)
        ]

    # ... (middle, right, full pagination tetap sama karena pakai add_button)

    @property
    def build_pagination(self):
        if self.count_pages <= 1: # Tambahkan handling jika cuma 1 halaman
             return [self.add_button(self.SYMBOL_CURRENT_PAGE.format(1), 1)]
             
        if self.count_pages <= 5:
            return self.full_pagination
        else:
            if self.current_page <= 3:
                return self.left_pagination
            elif self.current_page > self.count_pages - 3:
                return self.right_pagination
            else:
                return self.middle_pagination

    def row(self, *args):
        self.inline_keyboard.append([button for button in args])

    @property
    def markup(self):
        self.inline_keyboard.append(self.build_pagination)


class InlineButton(InlineKeyboardButton):
    def __init__(self, text=None, callback_data=None, url=None,
                 login_url=None, user_id=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, callback_game=None,
                 style=None): # <--- 1. Harus ada parameter style di sini
        super().__init__(
            text=text,
            callback_data=callback_data,
            url=url,
            login_url=login_url,
            user_id=user_id,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            callback_game=callback_game,
            style=style # <--- 2. Harus diteruskan ke super() di sini
        )


class ReplyButton(KeyboardButton):
    def __init__(self, text=None, request_contact=None, request_location=None, style=None): # Tambah style
        super().__init__(
            text=text,
            request_contact=request_contact,
            request_location=request_location,
            style=style # Kirim style ke sini
        )

class ReplyKeyboard(ReplyKeyboardMarkup):
    def __init__(self, resize_keyboard=True, one_time_keyboard=None,
                 selective=None, placeholder=None, row_width=3):
        self.keyboard = list()
        super().__init__(
            keyboard=self.keyboard,
            resize_keyboard=resize_keyboard, # Default True biar rapi
            one_time_keyboard=one_time_keyboard,
            selective=selective,
            placeholder=placeholder
        )
        self.row_width = row_width

    def add(self, *args):
        processed_btns = []
        for btn in args:
            # Jika input berupa list [text, style]
            if isinstance(btn, (list, tuple)):
                text = btn[0]
                style = btn[1] if len(btn) > 1 else None
                processed_btns.append(ReplyButton(text=text, style=style))
            else:
                processed_btns.append(btn)

        self.keyboard = [
            processed_btns[i:i + self.row_width]
            for i in range(0, len(processed_btns), self.row_width)
        ]

    def row(self, *args):
        processed_btns = []
        for btn in args:
            if isinstance(btn, (list, tuple)):
                text = btn[0]
                style = btn[1] if len(btn) > 1 else None
                processed_btns.append(ReplyButton(text=text, style=style))
            else:
                processed_btns.append(btn)
        self.keyboard.append(processed_btns)


class ReplyKeyboardRemove(ReplyKeyboardRemove):
    def __init__(self, selective=None):
        super().__init__(selective=selective)


class ForceReply(ForceReply):
    def __init__(self, selective=None, placeholder=None):
        super().__init__(selective=selective, placeholder=placeholder)