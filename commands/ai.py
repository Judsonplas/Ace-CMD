import aiohttp
import discord

from discord.ext import commands

from systems.config import (
    OLLAMA_URL,
    OLLAMA_MODEL
)

from systems.logger import log_command


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ai(
        self,
        ctx,
        *,
        prompt
    ):
        msg = "Thinking..."

        await ctx.send(msg)


        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }


        try:
            async with aiohttp.ClientSession() as session:

                async with session.post(
                    f"{OLLAMA_URL}/api/generate",
                    json=payload
                ) as response:

                    data = await response.json()


            answer = data.get(
                "response",
                "No response."
            )


        except Exception as e:

            answer = (
                "AI connection error:\n"
                f"{e}"
            )


        if len(answer) > 1900:
            answer = answer[:1900]


        await ctx.send(answer)


        log_command(
            ctx,
            answer
        )


async def setup(bot):
    await bot.add_cog(AI(bot))
