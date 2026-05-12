# Import Required Discord Library and Import(s).
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moderation = app_commands.Group(name="moderation", description="Moderation Commands")

    @moderation.command(name="kick", description="Kick a Member")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None):
        if interaction.user.guild_permissions.kick_members:
            if member.id == interaction.user.id:
                await interaction.response.send_message("⛔ You are Unable to Kick Yourself.", ephemeral=True)
                return
            if member.top_role >= interaction.user.top_role:
                await interaction.response.send_message("⛔ You are Unable to Kick someone of Equal or Higher Role.", ephemeral=True)
                return
            if reason is None:
                reason = "No Reason Provided"
            await interaction.response.send_message(f"✅ Successfully Kicked {member.display_name} from Server for: {reason}")
            await member.kick(reason=reason)
        else:
            await interaction.response.send_message("⛔ You do NOT have Permission to Use this Command.", ephemeral=True)
    
    @moderation.command(name="purge", description="Permanently Deleted x Amount of Messages in Channel")
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer()
        if interaction.user.guild_permissions.manage_messages:
            if amount < 1:
                await interaction.followup.send_message("⛔ Please Provide a Valid Amount of Messages to Purge.", ephemeral=True)
                return
            await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"✅ Successfully Purged {amount} Messages in this Channel.", ephemeral=True)
        else:
            await interaction.followup.send("⛔ You do NOT have Permission to Use this Command.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))