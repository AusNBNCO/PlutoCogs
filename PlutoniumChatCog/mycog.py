import discord
from discord.ext import tasks
from redbot.core import commands, Config
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
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild = {
            "channel_id": None,
            "log_file_path": None,
        }
        self.config.register_guild(**default_guild)
        self.observer = None
        self.handler = None
        self.last_position = 0

    async def read_log_file(self):
        guild = self.bot.guilds[0]
        channel_id = await self.config.guild(guild).channel_id()
        if not channel_id:
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            return

        log_file_path = await self.config.guild(guild).log_file_path()
        if not log_file_path:
            return

        try:
            with open(log_file_path, 'r') as file:
                file.seek(self.last_position)
                lines = file.readlines()
                self.last_position = file.tell()

            for line in 
