from pyrogram.emoji import (
    FLAG_UKRAINE, FLAG_UZBEKISTAN, FLAG_SPAIN, FLAG_TURKEY,
    FLAG_BELARUS, FLAG_GERMANY, FLAG_CHINA, FLAG_UNITED_KINGDOM,
    FLAG_FRANCE, FLAG_INDONESIA, FLAG_ITALY,
    FLAG_SOUTH_KOREA, FLAG_RUSSIA
)

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ForceReply as PyroForceReply,
    ReplyKeyboardRemove as PyroReplyKeyboardRemove
)

from typing import List, Union


# =========================
# SAFE STYLE (DISABLED)
# =========================
def get_style(style=None):
    return None


# =========================
# INLINE KEYBOARD BUILDER (IKB)
# =========================
def ikb(data):
    keyboard = []

    for row in data:
        buttons = []

        for btn in row:
            text = btn[0]
            value = btn[1]

            # URL button
            if isinstance(value, str) and value.startswith("http"):
                buttons.append(
                    InlineKeyboardButton(
                        text=text,
                        url=value
                    )
                )
            else:
                buttons.append(
                    InlineKeyboardButton(
                        text=text,
                        callback_data=str(value)
                    )
                )

        keyboard.append(buttons)

    return InlineKeyboardMarkup(keyboard)


# =========================
# REPLY KEYBOARD BUILDER (KB)
# =========================
def kb(data):
    keyboard = []

    for row in data:
        buttons = [
            KeyboardButton(text=str(btn))
            for btn in row
        ]
        keyboard.append(buttons)

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


# =========================
# INLINE KEYBOARD CLASS (ADVANCED)
# =========================
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
        self.inline_keyboard = []
        super().__init__(self.inline_keyboard)
        self.row_width = row_width

    def add(self, *args):
        self.inline_keyboard = [
            args[i:i + self.row_width]
            for i in range(0, len(args), self.row_width)
        ]

    def row(self, *args):
        self.inline_keyboard.append(list(args))

    # =========================
    # BUTTON BUILDER
    # =========================
    def _add_button(self, text, value):
        if isinstance(value, str) and value.startswith("http"):
            return InlineKeyboardButton(text=text, url=value)

        return InlineKeyboardButton(
            text=text,
            callback_data=str(value)
        )

    # =========================
    # PAGINATION
    # =========================
    def paginate(self, count_pages: int, current_page: int, callback_pattern: str):
        self.count_pages = count_pages
        self.current_page = current_page
        self.callback_pattern = callback_pattern

        self.inline_keyboard.append(self._build_pagination)
        return self

    @property
    def _full_pagination(self):
        return [
            self._add_button(
                str(i),
                self.callback_pattern.format(number=i)
            )
            for i in range(1, self.count_pages + 1)
        ]

    @property
    def _left_pagination(self):
        return [
            self._add_button(
                str(i),
                self.callback_pattern.format(number=i)
            )
            for i in range(1, min(6, self.count_pages + 1))
        ]

    @property
    def _middle_pagination(self):
        return [
            self._add_button("«", self.callback_pattern.format(number=1)),
            self._add_button("‹", self.callback_pattern.format(number=self.current_page - 1)),
            self._add_button(str(self.current_page), self.callback_pattern.format(number=self.current_page)),
            self._add_button("›", self.callback_pattern.format(number=self.current_page + 1)),
            self._add_button("»", self.callback_pattern.format(number=self.count_pages)),
        ]

    @property
    def _right_pagination(self):
        return [
            self._add_button("«", self.callback_pattern.format(number=1)),
            self._add_button(str(self.count_pages - 3), self.callback_pattern.format(number=self.count_pages - 3))
        ] + [
            self._add_button(str(i), self.callback_pattern.format(number=i))
            for i in range(self.count_pages - 2, self.count_pages + 1)
        ]

    @property
    def _build_pagination(self):
        if self.count_pages <= 5:
            return self._full_pagination
        elif self.current_page <= 3:
            return self._left_pagination
        elif self.current_page > self.count_pages - 3:
            return self._right_pagination
        else:
            return self._middle_pagination

    # =========================
    # LANGUAGES
    # =========================
    def languages(self, callback_pattern: str, locales: Union[str, List[str]], row_width: int = 2):
        locales = locales if isinstance(locales, list) else [locales]

        buttons = [
            InlineKeyboardButton(
                text=self._LOCALES.get(loc, "Invalid locale"),
                callback_data=callback_pattern.format(locale=loc)
            )
            for loc in locales
        ]

        self.inline_keyboard = [
            buttons[i:i + row_width]
            for i in range(0, len(buttons), row_width)
        ]


# =========================
# REPLY KEYBOARD WRAPPER
# =========================
class ReplyKeyboard(ReplyKeyboardMarkup):

    def __init__(self, resize_keyboard=True, one_time_keyboard=False,
                 selective=False, placeholder=None, row_width=3):

        self.keyboard = []
        super().__init__(
            keyboard=self.keyboard,
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective,
            placeholder=placeholder
        )
        self.row_width = row_width

    def add(self, *args):
        self.keyboard = [
            args[i:i + self.row_width]
            for i in range(0, len(args), self.row_width)
        ]

    def row(self, *args):
        self.keyboard.append(list(args))


# =========================
# SIMPLE BUTTON WRAPPERS
# =========================
class InlineButton(InlineKeyboardButton):
    pass


class ReplyButton(KeyboardButton):
    pass


class ReplyKeyboardRemove(PyroReplyKeyboardRemove):
    pass


class ForceReply(PyroForceReply):
    pass