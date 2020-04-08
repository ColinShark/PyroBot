import asyncio, io, os, sys, traceback
from asyncio import sleep

from pyrogram import Filters, Message
from pyrogram.errors import ChatSendMediaForbidden, FloodWait

from ..pyrobot import PyroBot
from ..utils import helpers


@PyroBot.on_message(Filters.me & Filters.command("eval", "!"))
async def evaluation(app: PyroBot, message: Message):
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, app, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "**EVAL**: ```{}```\n\n**OUTPUT**:\n```{}``` \n".format(
        cmd, evaluation.strip()
    )

    if len(final_output) > 4096:
        with open("eval.txt", "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await app.send_document(
            chat_id=message.chat.id,
            document="eval.txt",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove("eval.txt")
        await message.delete()
    else:
        await message.reply_text(final_output)


async def aexec(code, app, message):
    exec(
        f"async def __aexec(app, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](app, message)
