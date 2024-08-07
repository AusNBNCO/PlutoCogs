import discord
from discord.ext import tasks
from redbot.core import commands
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

class LogHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if event.src_path.endswith("chat.log"):
            asyncio.run_coroutine_threadsafe(self.callback(), asyncio.get_event_loop())

class PlutoniumChatCog(commands.Cog):
    """Cog for logging Plutonium server chat messages to Discord."""

    def __init__(self, bot):
        self.bot = bot
        self.log_file_path = os.getenv('LOG_FILE_PATH', 'path/to/your/chat.log')
        self.channel_id = int(os.getenv('DISCORD_CHANNEL_ID', 'your_discord_channel_id'))
        self.observer = Observer()
        self.handler = LogHandler(self.read_log_file)
        self.observer.schedule(self.handler, path=os.path.dirname(self.log_file_path), recursive=False)
        self.observer.start()
        self.last_position = 0

    async def read_log_file(self):
        channel = self.bot.get_channel(self.channel_id)
        with open(self.log_file_path, 'r') as file:
            file.seek(self.last_position)
            lines = file.readlines()
            self.last_position = file.tell()
        
        for line in lines:
            await channel.send(line.strip())

    def cog_unload(self):
        self.observer.stop()
        self.observer.join()

def setup(bot):
    bot.add_cog(PlutoniumChatCog(bot))
