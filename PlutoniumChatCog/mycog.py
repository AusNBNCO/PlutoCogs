import discord
from redbot.core import commands, Config

class PlutoniumChatCog(commands.Cog):
    """Minimal Cog for debugging."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild = {
            "channel_id": None,
            "log_file_path": None,
        }
        self.config.register_guild(**default_guild)

    @commands.command()
    async def ping(self, ctx):
        """A simple ping command to test the cog."""
        await ctx.send("Pong!")

def setup(bot):
    cog = PlutoniumChatCog(bot)
    bot.add_cog(cog)
    print("Cog setup complete.")
