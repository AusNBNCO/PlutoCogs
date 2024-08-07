from .mycog import PlutoniumChatCog

async def setup(bot):
    cog = PlutoniumChatCog(bot)
    await bot.add_cog(cog)
    print("Cog setup complete.")
