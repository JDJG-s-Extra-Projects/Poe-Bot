import discord
from discord import ui
from discord.ext import commands


class Confirm(discord.ui.View):
    def __init__(self, user, modal):
        super().__init__()
        self.user = user
        self.modal = modal

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):

        modal = self.modal.child(*self.modal.args)
        await interaction.response.send_modal(modal)

        # edit message to remove the buttons

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("I will stop the response for you", ephemeral=True)

        # edit message to remove the buttons

    async def on_timeout(self):
        await self.message.edit(content="you took too long", view=None)

    async def interaction_check(self, interaction):

        if interaction.user != self.user:
            await interaction.response.send_message("You can't do that")
            return False

        else:
            return True


class ServiceAsk(ui.Modal, title="Questionnaire Response"):
    question = ui.TextInput(label="Ask your Question", style=discord.TextStyle.paragraph)

    def __init__(self, ask_question, ai_client, child, **kwargs):

        self.ai_client = ai_client
        self.service = ask_question

        self.args = (ask_question, ai_client, child)
        self.child = child

        super().__init__(**kwargs)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Thank You now sending the response to the ai.", ephemeral=True)

        chunks = await self.ai_client(self.service, self.question.value)

        pag = commands.Paginator(prefix="", suffix="")

        for chunk in chunks:
            pag.add_line(chunk["response"])

        pages = pag.pages

        for page in pages:
            await interaction.followup.send(content=page, ephemeral=True)

        modal = self.child(*self.args)
        view = utils.Confirm(interaction.user, modal)

        view.message = await interaction.followup.send(
            content="Would you would like to ask another question?", view=view, ephemeral=True
        )
