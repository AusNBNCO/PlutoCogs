import discord
from redbot.core import commands

class PlutoniumChatCog(commands.Cog):
    """Minimal Cog for debugging."""

    def __init__(self, bot):
        self.bot = bot
        print("PlutoniumChatCog initialized")

    @commands.command()
    async def ping(self, ctx):
        """A simple ping command to test the cog."""
        await ctx.send("Pong!")
        print("Ping command executed")

async def setup(bot):
    print("Setting up cog")
    cog = PlutoniumChatCog(bot)
    await bot.add_cog(cog)
    print("Cog setup complete")
