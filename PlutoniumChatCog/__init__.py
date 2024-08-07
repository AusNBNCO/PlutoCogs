from .mycog import PlutoniumChatCog

async def setup(bot):
    try:
        print("Setting up cog")
        cog = PlutoniumChatCog(bot)
        await bot.add_cog(cog)
        print("Cog setup complete")
    except Exception as e:
        print(f"Error in setup: {e}")
