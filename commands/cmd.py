import asyncio

from discord.ext import commands

from systems.permissions import is_owner
from systems.logger import log_command


class Cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cmd(self, ctx, *, command=None):
        if not is_owner(ctx.author):
            return await ctx.send("Owner only.")

        if not command:
            return await ctx.send("Usage: $cmd <real shell command>")

        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()
        output = (stdout or stderr).decode(errors="ignore")

        if not output:
            output = f"Command finished with code {process.returncode}"

        await ctx.send(f"```\n{output[:1900]}\n```")
        log_command(ctx, command)


async def setup(bot):
    await bot.add_cog(Cmd(bot))
