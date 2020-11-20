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

from datetime import datetime

import speedtest
from pyrogram import filters
from pyrogram.types import Message

from pyrobot.pyrobot import PyroBot

SPEED_TEXT = [
    "`Running speed test...`",
    "`Getting best server based on ping...`",
    "`Testing download speed...`",
    "`Testing upload speed...`",
    "`Getting results and preparing formatting...`",
]
SPEEDTEST = (
    "Speedtest started: `{start}`\n\n"
    "Ping: `{ping} ms`\n"
    "Download: `{download}`\n"
    "Upload: `{upload}`\n"
    "ISP: __{isp}__"
)


def speed_convert(size):
    power = 2 ** 10
    zero = 0
    units = {
        0: "",
        1: "Kbit/s",
        2: "Mbit/s",
        3: "Gbit/s",
        4: "Tbit/s",
    }
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@PyroBot.on_message(filters.command("speed", "?") & filters.me)
async def i_am_speed(bot: PyroBot, message: Message):
    await message.edit_text("\n".join(SPEED_TEXT[:1]))
    speed = speedtest.Speedtest()

    for i, x in enumerate(
        [speed.get_best_server, speed.download, speed.upload, speed.results.dict]
    ):
        await message.edit_text("\n".join(SPEED_TEXT[: i + 2]))
        results = x()

    speed_message = SPEEDTEST.format(
        start=results["timestamp"],
        ping=results["ping"],
        download=speed_convert(results["download"]),
        upload=speed_convert(results["upload"]),
        isp=results["client"]["isp"],
    )
    await message.edit_text(speed_message)


@PyroBot.on_message(filters.command("ping", "?") & filters.me)
async def ping_me(bot: PyroBot, message: Message):
    start = datetime.now()
    await message.edit_text("`Pong!`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await message.edit_text(f"**Pong!**\n`{ms} ms`")
