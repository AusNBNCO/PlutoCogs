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
        if channel_id is None:
            return

        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return

        log_file_path = await self.config.guild(guild).log_file_path()
        if log_file_path is None:
            return

        try:
            with open(log_file_path, 'r') as file:
                file.seek(self.last_position)
                lines = file.readlines()
                self.last_position = file.tell()

            for line in lines:
                await channel.send(line.strip())
        except Exception as e:
            print(f"Error reading log file: {e}")

    @commands.command()
    async def setlogchannel(self, ctx, channel: discord.TextChannel):
        """Set the channel where chat logs will be sent."""
        await self.config.guild(ctx.guild).channel_id.set(channel.id)
        await ctx.send(f"Chat log channel set to {channel.mention}")
        await self.start_observer(ctx.guild)

    @commands.command()
    async def setlogpath(self, ctx, path: str):
        """Set the path to the chat log file."""
        await self.config.guild(ctx.guild).log_file_path.set(path)
        await ctx.send(f"Chat log file path set to {path}")
        await self.start_observer(ctx.guild)

    async def start_observer(self, guild):
        log_file_path = await self.config.guild(guild).log_file_path()
        if log_file_path is None:
            return

        if self.observer:
            self.observer.stop()
            self.observer.join()

        self.handler = LogHandler(self.read_log_file)
        self.observer = Observer()
        self.observer.schedule(self.handler, path=os.path.dirname(log_file_path), recursive=False)
        self.observer.start()

    def cog_unload(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
