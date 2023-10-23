import discord
from discord import app_commands
from discord.app_commands import Choice


class Ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_unload(self):
        return
        # use for later.


async def setup(bot):
    await bot.add_cog(Ai(bot))
