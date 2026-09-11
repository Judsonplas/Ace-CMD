import os
import asyncio

import discord

from discord.ext import commands
from dotenv import load_dotenv

from systems.database import ensure_files


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "$"


intents = discord.Intents.all()


bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    print("=" * 50)
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("=" * 50)


async def load_extensions():

    extensions = [
        "commands.owner",
        "commands.admin",
        "commands.moderation",
        "commands.roles",
        "commands.ai",
        "commands.utility",
        "commands.cmd"
    ]


    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f"[OK] Loaded {extension}")

        except Exception as e:
            print(f"[FAIL] {extension}")
            print(type(e).__name__)
            print(e)


async def main():

    ensure_files()

    async with bot:
        await load_extensions()

        if TOKEN is None:
            print("ERROR: DISCORD_TOKEN missing from .env")
            return

        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
