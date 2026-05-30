# Import Required Discord Library and Import(s).
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import datetime

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

            embed = discord.Embed(
            title="Moderation Action - Kick",
            description=(
            f"**User:** {member.mention} (`{member.id}`)\n"
            f"**Moderator:** {interaction.user.mention}\n"
            f"**Reason:** {reason}"
            ),
            color=discord.Color.orange()
        )

            await interaction.response.send_message(embed=embed)
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

    @moderation.command(name="ban", description="Ban a Member")
    async def ban(self, interaction:discord.Interaction, member: discord.Member, reason: Optional[str] = None):
        if interaction.user.guild_permissions.ban_members:
            if member.id == interaction.user.id:
                await interaction.response.send_message("⛔ You are Unable to Ban Yourself.", ephemeral=True)
                return
            if member.top_rule >= interaction.user.top_role:
                await interaction.response.send_message("⛔ You are Unable to Ban someone of Equal or Higher Role", ephemeral=True)
                return
            if reason is None:
                reason = "No Reason Provided"

            embed = discord.Embed(
            title="Moderation Action - Ban",
            description=(
            f"**User:** {member.mention} (`{member.id}`)\n"
            f"**Moderator:** {interaction.user.mention}\n"
            f"**Reason:** {reason}"
            ),
            color=discord.Color.red()
        )

            await interaction.response.send_message(embed=embed)
            await member.ban(reason=reason)
        else:
            await interaction.response.send_message("⛔ You do NOT have Permission to use this Command.", ephemeral=True)
    
    @moderation.command(name="timeout", description="Timeout a Member")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None, duration: Optional[int] = 10):
        duration = datetime.timedelta(minutes=duration)
        if interaction.user.guild_permissions.moderate_members:
            if member.id == interaction.user.id:
                await interaction.response.send_message("⛔ You are Unable to Timeout Yourself.", ephemeral=True)
                return
            if member.top_role >= interaction.user.top_role:
                await interaction.response.send_message("⛔ You are Unable to Timeout someone of Equal or Higher Role", ephemeral=True)
                return
            if reason is None:
                reason = "No Reason Provided"

            embed = discord.Embed(
            title="Moderation Action - Timeout",
            description=(
            f"**User:** {member.mention} (`{member.id}`)\n"
            f"**Moderator:** {interaction.user.mention}\n"
            f"**Reason:** {reason}\n"
            f"**Duration:** {duration}"
            ),
            color=discord.Color.orange()
        )

            await interaction.response.send_message(embed=embed)    
            await member.timeout(duration, reason=reason)
        else:
            await interaction.response.send_message("⛔ You do NOT have Permission to use this Command.", ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))