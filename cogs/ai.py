import asyncio
import typing
import os

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from discord import ui

from poe_api_wrapper import PoeApi, api


class Ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.free_bots = []
        self.loose_bots = []
        self.restricted_bots = []
        self.client = None

    def grab_names(self):
        token = os.environ["API_TOKEN"]
        client = PoeApi(token)

        self.client = client

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

        return (free_bots, loose_bots, restricted_bots)

    async def cog_load(self):
        self.free_bots, self.loose_bots, self.restricted_bots = await asyncio.to_thread(self.grab_names)

    async def cog_unload(self):
        return
        # use for later.

    
    def ask(self, service, question):

        resp = client.send_message(service, question)

        # this chunked therefore it will not be put together with commands.Paginator

        return resp
    
    async def ask_question(self, bot, question):

        return await asyncio.to_thread(self.ask)
    
    class ServiceAsk(ui.Modal, title='Questionnaire Response'):
        question = ui.TextInput(label='Ask your Question')

        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.send_message(f"Thank You now sending the response to the ai.", ephemeral=True)

            chunks = await self.ai_client(self.service, self.question) 

            pag = commands.Paginator(prefix="", suffix="")

            for chunk in chunks:
                pag.add_line(chunk["response"])

            
            pages = pag.pages

            for page in pages:
                await interaction.response.followup(content=page)

            view.message = await interaction.response.followup(content="Would you would like to ask another question?", ephemeral=True)

            # add buttons in a bit to confirm or deny

            # view.message is to get the message for the view to be able to edit
    
    @app_commands.command(description="Talk to AI", name="talk")
    async def talk(self, interaction : discord.Interaction, bot: typing.Optional[str]):

        bots = self.free_bots

        if not bot:
            return await interaction.response.send_message(content=f"Please choose a bot")

        if bot not in bots:

            return await interaction.response.send_message(content=f"The bot you looked up was not found")

        modal = self.ServiceAsk()
        modal.ai_client = self.ask_question
        modal.service = bot

        await interaction.response.send_modal(modal)

    
    @talk.autocomplete("bot")
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):

        bots = self.free_bots

        all_choices = [Choice(name=bot, value=bot) for bot in bots]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith


async def setup(bot):
    await bot.add_cog(Ai(bot))