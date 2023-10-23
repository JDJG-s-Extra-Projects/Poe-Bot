import os
import traceback
from typing import Any

import discord
from cogs import EXTENSIONS
from discord.ext import commands
from dotenv import load_dotenv


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


load_dotenv()

bot = ApiBot(command_prefix=commands.when_mentioned_or("a$"), intents=discord.Intents.all())

@bot.event
async def on_ready():

    print(bot.user)
    print(bot.user.id)
    print("Bot Booted up properly :)")

bot.run(os.environ["TOKEN"])
