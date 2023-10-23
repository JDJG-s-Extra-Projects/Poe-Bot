import asyncio

import discord
from discord import app_commands
from discord.app_commands import Choice
from poe_api_wrapper import PoeApi, api


class Ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.free_bots = []
        self.loose_bots = []
        self.restricted_bots = []

    def grab_names(self):
        token = os.environ["API_TOKEN"]
        client = PoeApi(token)
        bots = client.get_available_bots()
        free_bots = sorted(filter(lambda b: not bots[b]["bot"]["isLimitedAccess"], bots))
        loose_bots = sorted(
            filter(
                lambda b: bots[b]["bot"]["isLimitedAccess"] and bots[b]["bot"]["limitedAccessType"] == "soft_limit",
                bots,
            )
        )

        restricted_bots = sorted(
            filter(
                lambda b: bots[b]["bot"]["isLimitedAccess"] and bots[b]["bot"]["limitedAccessType"] == "hard_limit",
                bots,
            )
        )

        return (free_bots, loose_bots, resticted_bots)

    async def cog_load(self):
        self.free_bots, self.loose_bots, self.restricted_bots = await asyncio.to_thread(self.grab_names)

    async def cog_unload(self):
        return
        # use for later.


async def setup(bot):
    await bot.add_cog(Ai(bot))