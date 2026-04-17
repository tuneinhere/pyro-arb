#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>

from pyrogram import raw, types
from ..object import Object

class KeyboardButton(Object):
    """One button of the reply keyboard."""

    def __init__(
        self,
        text: str,
        request_contact: bool = None,
        request_location: bool = None,
        web_app: "types.WebAppInfo" = None,
        style: "pyrogram.enums.ButtonStyle" = None # --- MODIFIKASI: Tambah style
    ):
        super().__init__()

        self.text = str(text)
        self.request_contact = request_contact
        self.request_location = request_location
        self.web_app = web_app
        self.style = style # --- MODIFIKASI: Simpan style

    @staticmethod
    def read(b):
        if isinstance(b, raw.types.KeyboardButton):
            return b.text

        if isinstance(b, raw.types.KeyboardButtonRequestPhone):
            return KeyboardButton(
                text=b.text,
                request_contact=True
            )

        if isinstance(b, raw.types.KeyboardButtonRequestGeoLocation):
            return KeyboardButton(
                text=b.text,
                request_location=True
            )

        if isinstance(b, raw.types.KeyboardButtonSimpleWebView):
            return KeyboardButton(
                text=b.text,
                web_app=types.WebAppInfo(
                    url=b.url
                )
            )

    def write(self):
        # --- MODIFIKASI: Tambahkan style=self.style pada setiap return raw ---
        
        if self.request_contact:
            return raw.types.KeyboardButtonRequestPhone(
                text=self.text, 
                style=self.style
            )
        elif self.request_location:
            return raw.types.KeyboardButtonRequestGeoLocation(
                text=self.text, 
                style=self.style
            )
        elif self.web_app:
            return raw.types.KeyboardButtonSimpleWebView(
                text=self.text, 
                url=self.web_app.url, 
                style=self.style
            )
        else:
            return raw.types.KeyboardButton(
                text=self.text, 
                style=self.style
            )
