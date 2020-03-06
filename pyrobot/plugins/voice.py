# PyroBot - Telegram Userbot powered by Pyrogram
# Copyright (C) 2020 - Nicolas "ColinShark" Neht

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import time

import gtts
from pyrogram import Filters, Message
from pyrogram.errors import ChatSendMediaForbidden

from ..pyrobot import PyroBot
from ..utils import helpers

gtts_langs = gtts.lang.tts_langs()


@PyroBot.on_message(Filters.me & Filters.command("v", "!"))
def alive(app: PyroBot, message: Message):
    if len(message.command) == 1:
        message.delete()
        return

    if message.command[-1] not in gtts_langs:
        language = "en"
        words_to_say = " ".join(message.command[1:])
    else:
        language = message.command[-1]
        words_to_say = " ".join(message.command[1:-1])

    speech = gtts.gTTS(words_to_say, lang=language)
    speech.save("text_to_speech.oog")
    try:
        app.send_voice(
            chat_id=message.chat.id,
            voice="text_to_speech.oog",
            reply_to_message_id=helpers.reply_id(message),
        )
    except ChatSendMediaForbidden:
        message.edit_text(
            "Voice Messages aren't allowed here.\nCopy sent to Saved Messages."
        )
        app.send_voice(chat_id="me", voice="text_to_speech.oog", caption=words_to_say)
        time.sleep(2)
    try:
        os.remove("text_to_speech.oog")
    except FileNotFoundError:
        pass
    message.delete()
