import discord

class Confirm(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.user = user
    
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):

        modal = self.modal
        modal.child = self.modal_copy

        await interaction.response.send_modal(modal)
        

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("I will stop the response for you", ephemeral=True)
    
    async def on_timeout(self):
        await self.message.edit(content="you took too long", view=None)

    async def interaction_check(self, interaction):

        if interaction.user != self.user:
            await interaction.response.send_message("You can't do that")
            return False

        else:
            return True