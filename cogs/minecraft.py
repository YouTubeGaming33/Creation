# Import Required Discord Library and Import(s).
import discord
from discord.ext import commands
from discord import app_commands
from misc.helper import pull_users
import math

class PlayerPaginator(discord.ui.View):
    def __init__(self, players, per_page=20):
        super().__init__(timeout=60)
        self.players = players
        self.per_page = per_page
        self.current_page = 1
        self.max_pages = math.ceil(len(players) / per_page) or 1
        self.update_buttons()

    # Disables/Enables buttons based on the current page.
    # E.g. Disables "Previous" on Page 1 and "Next" on the Last Page.
    def update_buttons(self):
        self.prev_button.disabled = (self.current_page == 1)
        self.next_button.disabled = (self.current_page == self.max_pages)

    # Creates Embed for the Current Page of Players.
    # Max of 20 Players Per Page to Avoid Clutter.
    def create_embed(self):
        start = (self.current_page - 1) * self.per_page
        end = start + self.per_page
        subset = self.players[start:end]
        
        player_list_str = "\n".join([f"**{i+1}.** {name}" for i, name in enumerate(subset, start=start)])
        
        embed = discord.Embed(
            title="# Players Online",
            description=player_list_str if subset else "No players currently visible.",
            color=0x2ecc71
        )
        embed.set_footer(text=f"Page {self.current_page} of {self.max_pages} • Total: {len(self.players)}")
        return embed

    # Previous Button - Goes Back a Page and Updates the Embed.
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    # Next Button - Goes Forward a Page and Updates the Embed.
    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

# Class for Minecraft Cog.
class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    minecraft = app_commands.Group(name="minecraft", description="Minecraft Commands")

    @minecraft.command(name="debug", description="Debug Command to Test API Response")
    async def debug(self, interaction: discord.Interaction):
        channel_id = 1503046380435013843  # Replace with your actual ID
        channel = self.bot.get_channel(channel_id)

        if channel:
            await channel.send("Hello! This is a message to a specific channel.")

    @minecraft.command(name="players", description="List online players")
    async def players(self, interaction: discord.Interaction):
        await interaction.response.defer() 
        
        usernames = pull_users()

        if not usernames:
            await interaction.followup.send("No Players Online!", ephemeral=True)
        else:
            view = PlayerPaginator(usernames)
            await interaction.followup.send(embed=view.create_embed(), view=view)

async def setup(bot):
    await bot.add_cog(Minecraft(bot))