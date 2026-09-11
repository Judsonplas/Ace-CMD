import asyncio

from discord.ext import commands

from systems.permissions import is_owner
from systems.logger import log_command


class Cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def cmd(
        self,
        ctx,
        *,
        command=None
    ):
        if not is_owner(ctx.author):
            return await ctx.send(
                "Owner only."
            )


        if not command:
            return await ctx.send(
                "Usage: $cmd <terminal command>"
            )


        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )


            stdout, stderr = await process.communicate()


            output = (
                stdout.decode(errors="ignore")
                if stdout
                else stderr.decode(errors="ignore")
            )


            if not output:
                output = (
                    f"Command finished "
                    f"with code {process.returncode}"
                )


            if len(output) > 1900:
                output = output[:1900]


            await ctx.send(
                f"```\n{output}\n```"
            )


            log_command(
                ctx,
                command
            )


        except Exception as e:

            await ctx.send(
                f"Error:\n```\n{e}\n```"
            )


async def setup(bot):
    await bot.add_cog(Cmd(bot))
