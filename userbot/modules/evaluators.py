# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for executing code and terminal commands from Telegram. """

import asyncio
import re
from os import remove

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, TERM_ALIAS
from userbot.events import register

@register(outgoing=True, pattern=r"^\.term(?: |$|\n)(.*)")
async def terminal_runner(term):
    """ For .term command, runs bash commands and scripts on your server. """
    curruser = TERM_ALIAS
    command = term.pattern_match.group(1)
    try:
        from os import geteuid

        uid = geteuid()
    except ImportError:
        uid = "This ain't it chief!"

    if term.is_channel and not term.is_group:
        return await term.edit("Term commands aren't permitted on channels!")

    if not command:
        return await term.edit(
            " Give a command or use .help term for an example."
        )

    for i in ("userbot.session", "env"):
        if command.find(i) != -1:
            return await term.edit("That's a dangerous operation! Not Permitted!")

    if not re.search(r"echo[ \-\w]*\$\w+", command) is None:
        return await term.edit("That's a dangerous operation! Not Permitted!")

    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

    if len(result) > 4096:
        with open("output.txt", "w+") as output:
            output.write(result)
        await term.client.send_file(
            term.chat_id,
            "output.txt",
            reply_to=term.id,
            caption="Output too large, sending as file",
        )
        remove("output.txt")
        return

    if uid == 0:
        await term.edit("" f"{curruser}:~# {command}" f"\n{result}" "")
    else:
        await term.edit("" f"{curruser}:~$ {command}" f"\n{result}" "")

    if BOTLOG:
        await term.client.send_message(
            BOTLOG_CHATID, "Terminal command " + command + " was executed sucessfully.",
        )


CMD_HELP.update({
                 "term": ">.term <cmd>"
                 "\nUsage: Run bash commands and scripts on your server.",
                 })
