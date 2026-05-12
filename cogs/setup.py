# Import Required Discord Library and Import(s).
import discord
from discord.ext import commands, tasks
from discord import app_commands
from misc.helper import pull_status

# Class for Setup Cog.
class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Start the background task when the Cog loads
        self.update_status_task.start()

    def cog_unload(self):
        # Stop the task if the Cog is unloaded to prevent memory leaks
        self.update_status_task.cancel()

    @tasks.loop(minutes=1)
    async def update_status_task(self):
        await self.bot.wait_until_ready()
        
        # Get the detailed status
        status_data = pull_status()
        is_online = status_data["online"]
        
        if is_online:
            status_text = "🟢 Online"
            status_color = 0x2ecc71 # Green
        else:
            status_text = "🔴 Offline"
            status_color = 0xe74c3c # Red
            player_count = 0

        embed = discord.Embed(
            title="🌐 Server Status",
            description=f"**Status:** {status_text}",
            color=status_color
        )
        embed.set_footer(text="Auto-updates every 10 minutes")

        # 5. Fetch and edit the message
        try:
            channel = self.bot.get_channel(1503046380435013843)
            if channel:
                message = await channel.fetch_message(1503052217807016036)
                await message.edit(content=None, embed=embed)
        except Exception as e:
            print(f"Failed to update status message: {e}")

    @update_status_task.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Setup(bot))