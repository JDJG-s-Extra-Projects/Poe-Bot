import os
import sys
import traceback
from typing import Any

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import EXTENSIONS


class ApiBot(commands.Bot):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        for cog in EXTENSIONS:
            try:
                await self.load_extension(f"{cog}")
            except commands.errors.ExtensionError:
                traceback.print_exc()

            await self.load_extension("jishaku")

    async def on_error(self, event, *args: Any, **kwargs: Any) -> None:
        more_information = sys.exc_info()
        error_wanted = traceback.format_exc()
        traceback.print_exc()

        # print(event)
        # print(more_information[0])
        # print(args)
        # print(kwargs)


load_dotenv()
# something cool is that you can pass filenames into here.

bot = ApiBot(command_prefix=commands.when_mentioned_or("a$"), intents=discord.Intents.all())


@bot.event
async def on_ready():

    print(bot.user)
    print(bot.user.id)
    print("Bot Booted up properly :)")


bot.run(os.environ["TOKEN"])
