import discord

class Confirm(discord.ui.View):
    def __init__(self, user, modal):
        super().__init__()
        self.user = user
        self.modal = modal
    
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):

        modal = self.modal.child(*self.modal.args)
        await interaction.response.send_modal(modal)

        # edit message to remove the buttons

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
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