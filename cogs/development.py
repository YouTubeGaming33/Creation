# Import Required Discord Library and Import(s).
import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Development(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.now(datetime.timezone.utc)

    development = app_commands.Group(name="development", description="Development Commands")

    @development.command(name="status", description="Check the bot's current latency and uptime status")
    async def status(self, interaction: discord.Interaction):
        is_admin = interaction.user.guild_permissions.administrator
        is_owner = interaction.user.id == interaction.guild.owner_id

        if is_admin or is_owner:
            ping = round(self.bot.latency * 1000)

            current_time = datetime.datetime.now(datetime.timezone.utc)
            uptime_duration = current_time - self.start_time

            days = uptime_duration.days
            hours, remainder = divmod(uptime_duration.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            uptime_str = ""
            if days > 0:
                uptime_str += f"{days}d "
            if hours > 0 or days > 0:
                uptime_str += f"{hours}h "
            uptime_str += f"{minutes}m {seconds}s"

            if ping < 150:
                status_color = discord.Color.green()
                ping_emoji = "🟢"
            elif ping < 290:
                status_color = discord.Color.orange()
                ping_emoji = "🟡"
            else:
                status_color = discord.Color.red()
                ping_emoji = "🔴"

            embed = discord.Embed(
                title="⚙️ System Status",
                color=status_color
            )
            embed.add_field(name="Ping / Latency", value=f"{ping_emoji} `{ping}ms`", inline=True)
            embed.add_field(name="Uptime", value=f"⏳ `{uptime_str}`", inline=True)
            embed.set_footer(text=f"Requested by {interaction.user.name}")
            embed.timestamp = interaction.created_at

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("⛔ You do NOT have Permission to use this Command.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Development(bot))