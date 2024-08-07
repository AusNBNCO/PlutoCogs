from .mycog import PlutoniumChatCog

def setup(bot):
    cog = PlutoniumChatCog(bot)
    bot.add_cog(cog)
