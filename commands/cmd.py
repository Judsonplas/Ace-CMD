import asyncio
import os

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
            return await ctx.send("Usage: $cmd <command>")

        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.getcwd()
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=30
            )

            output = stdout.decode(errors="ignore") or stderr.decode(errors="ignore")
            if not output:
                output = f"Exit code: {process.returncode}"

        except asyncio.TimeoutError:
            return await ctx.send("Command timed out.")
        except Exception as e:
            return await ctx.send(str(e))

        await ctx.send("```\n" + output[:1900] + "\n```")
        log_command(ctx, command)


async def setup(bot):
    await bot.add_cog(Cmd(bot))
