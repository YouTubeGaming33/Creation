# Import Required Discord Library and Import(s).
import discord
from discord.ext import commands, tasks
from discord import app_commands
from misc.helper import pull_status

# Class for Setup Cog.
class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_status_task.start()

    def cog_unload(self):
        self.update_status_task.cancel()

    @tasks.loop(minutes=10)
    async def update_status_task(self):
        await self.bot.wait_until_ready()
        
        status_data = pull_status()
        is_online = status_data.get("online", False)
        
        if is_online:
            status_text = "🟢 Online"
            status_color = 0x2ecc71
            
            players_data = status_data.get('players', {})
            player_count = players_data.get('online', 0)
            max_players = players_data.get('max', 0)
            
            player_list = players_data.get('list', [])
            if player_list:
                usernames = [player['name'] for player in player_list]
                player_list_str = ", ".join(usernames)
            else:
                player_list_str = "Names hidden or unavailable"

            description = (
                f"**Status:** {status_text}\n"
                f"**Players:** {player_count}/{max_players}\n\n"
                f"**Online Players:**\n`{player_list_str}`"
            )
        else:
            status_text = "🔴 Offline"
            status_color = 0xe74c3c
            description = f"**Status:** {status_text}\n\nThe server is currently down."

        embed = discord.Embed(
            title="🌐 Server Status",
            description=description,
            color=status_color
        )
        embed.set_footer(text="Auto-updates every 10 minutes")

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