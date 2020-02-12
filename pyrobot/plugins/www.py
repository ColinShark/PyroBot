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
from pyrogram import Filters, Message

from ..pyrobot import PyroBot

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


@PyroBot.on_message(Filters.command("speed", "?") & Filters.me)
def i_am_speed(bot: PyroBot, message: Message):
    message.edit_text("\n".join(SPEED_TEXT[:1]))
    speed = speedtest.Speedtest()

    for i, x in enumerate(
        [speed.get_best_server, speed.download, speed.upload, speed.results.dict]
    ):
        message.edit_text("\n".join(SPEED_TEXT[: i + 2]))
        results = x()

    speed_message = SPEEDTEST.format(
        start=results["timestamp"],
        ping=results["ping"],
        download=speed_convert(results["download"]),
        upload=speed_convert(results["upload"]),
        isp=results["client"]["isp"],
    )
    message.edit_text(speed_message)
