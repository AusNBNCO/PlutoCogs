import discord
from redbot.core import commands

class PlutoniumChatCog(commands.Cog):
    """Minimal Cog for debugging."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """A simple ping command to test the cog."""
        await ctx.send("Pong!")

def setup(bot):
    bot.add_cog(PlutoniumChatCog(bot))
    print("Cog setup complete.")
