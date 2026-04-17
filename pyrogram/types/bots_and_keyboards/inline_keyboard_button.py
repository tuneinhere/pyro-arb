#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>

from typing import Union, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object

class InlineKeyboardButton(Object):
    """One button of an inline keyboard."""

    def __init__(
        self,
        text: str,
        callback_data: Union[str, bytes] = None,
        url: str = None,
        web_app: "types.WebAppInfo" = None,
        login_url: "types.LoginUrl" = None,
        user_id: int = None,
        switch_inline_query: str = None,
        switch_inline_query_current_chat: str = None,
        callback_game: "types.CallbackGame" = None,
        copy_text: Optional[str] = None,
        style: "pyrogram.enums.ButtonStyle" = None # --- MODIFIKASI: Tambah style
    ):
        super().__init__()

        self.text = str(text)
        self.callback_data = callback_data
        self.url = url
        self.web_app = web_app
        self.login_url = login_url
        self.user_id = user_id
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.copy_text = copy_text
        self.style = style # --- MODIFIKASI: Simpan style

    @staticmethod
    def read(b: "raw.base.KeyboardButton"):
        # Logika pembacaan tombol (read) tetap sama
        if isinstance(b, raw.types.KeyboardButtonCallback):
            try:
                data = b.data.decode()
            except UnicodeDecodeError:
                data = b.data
            return InlineKeyboardButton(text=b.text, callback_data=data)

        if isinstance(b, raw.types.KeyboardButtonUrl):
            return InlineKeyboardButton(text=b.text, url=b.url)

        if isinstance(b, raw.types.KeyboardButtonUrlAuth):
            return InlineKeyboardButton(text=b.text, login_url=types.LoginUrl.read(b))

        if isinstance(b, raw.types.KeyboardButtonUserProfile):
            return InlineKeyboardButton(text=b.text, user_id=b.user_id)

        if isinstance(b, raw.types.KeyboardButtonSwitchInline):
            if b.same_peer:
                return InlineKeyboardButton(text=b.text, switch_inline_query_current_chat=b.query)
            else:
                return InlineKeyboardButton(text=b.text, switch_inline_query=b.query)

        if isinstance(b, raw.types.KeyboardButtonGame):
            return InlineKeyboardButton(text=b.text, callback_game=types.CallbackGame())

        if isinstance(b, raw.types.KeyboardButtonWebView):
            return InlineKeyboardButton(text=b.text, web_app=types.WebAppInfo(url=b.url))

        if isinstance(b, raw.types.KeyboardButtonCopy):
            return InlineKeyboardButton(text=b.text, copy_text=b.copy_text)

        if isinstance(b, raw.types.KeyboardButton):
            return InlineKeyboardButton(text=b.text)

    async def write(self, client: "pyrogram.Client"):
        # --- MODIFIKASI: Menambahkan style=self.style pada setiap return raw ---
        
        if self.callback_data is not None:
            data = bytes(self.callback_data, "utf-8") if isinstance(self.callback_data, str) else self.callback_data
            return raw.types.KeyboardButtonCallback(
                text=self.text,
                data=data,
                style=self.style # Suntikkan style
            )

        if self.url is not None:
            return raw.types.KeyboardButtonUrl(
                text=self.text,
                url=self.url,
                style=self.style # Suntikkan style
            )

        if self.login_url is not None:
            return await self.login_url.write(
                text=self.text,
                bot=await client.resolve_peer(self.login_url.bot_username or "self"),
                style=self.style # Suntikkan style
            )

        if self.user_id is not None:
            return raw.types.InputKeyboardButtonUserProfile(
                text=self.text,
                user_id=await client.resolve_peer(self.user_id),
                style=self.style # Suntikkan style
            )

        if self.switch_inline_query is not None:
            return raw.types.KeyboardButtonSwitchInline(
                text=self.text,
                query=self.switch_inline_query,
                style=self.style # Suntikkan style
            )

        if self.switch_inline_query_current_chat is not None:
            return raw.types.KeyboardButtonSwitchInline(
                text=self.text,
                query=self.switch_inline_query_current_chat,
                same_peer=True,
                style=self.style # Suntikkan style
            )

        if self.callback_game is not None:
            return raw.types.KeyboardButtonGame(
                text=self.text,
                style=self.style # Suntikkan style
            )

        if self.web_app is not None:
            return raw.types.KeyboardButtonWebView(
                text=self.text,
                url=self.web_app.url,
                style=self.style # Suntikkan style
            )
        
        if self.copy_text is not None:
            return raw.types.KeyboardButtonCopy(
                text=self.text,
                copy_text=self.copy_text,
                style=self.style # Suntikkan style
            )
