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

from pyrogram import Filters, Message
from pyrogram.api.functions.messages import MarkDialogUnread

from ..pyrobot import PyroBot


@PyroBot.on_message(Filters.command("un", ".") & Filters.me)
async def unread_chat(app: PyroBot, message: Message):
    await message.delete()
    await app.send(
        MarkDialogUnread(peer=await app.resolve_peer(message.chat.id), unread=True)
    )
