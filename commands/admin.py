import discord

from discord.ext import commands

from systems.database import get_server_config
from systems.permissions import is_mod
from systems.logger import log_command


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def lock(self, ctx):
        config = get_server_config(
            ctx.guild.id
        )

        if not is_mod(ctx.author, config):
            return await ctx.send(
                "No permission."
            )


        await ctx.channel.set_permissions(
            ctx.guild.default_role,
            send_messages=False
        )


        msg = "Channel locked."

        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @commands.command()
    async def unlock(self, ctx):
        config = get_server_config(
            ctx.guild.id
        )

        if not is_mod(ctx.author, config):
            return await ctx.send(
                "No permission."
            )


        await ctx.channel.set_permissions(
            ctx.guild.default_role,
            send_messages=True
        )


        msg = "Channel unlocked."

        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @commands.command()
    async def slowmode(
        self,
        ctx,
        seconds: int
    ):
        config = get_server_config(
            ctx.guild.id
        )

        if not is_mod(ctx.author, config):
            return await ctx.send(
                "No permission."
            )


        await ctx.channel.edit(
            slowmode_delay=seconds
        )


        msg = (
            f"Slowmode set to "
            f"{seconds} seconds."
        )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @commands.command()
    async def clear(
        self,
        ctx,
        amount: int
    ):
        config = get_server_config(
            ctx.guild.id
        )

        if not is_mod(ctx.author, config):
            return await ctx.send(
                "No permission."
            )


        deleted = await ctx.channel.purge(
            limit=amount + 1
        )


        msg = (
            f"Deleted "
            f"{len(deleted)-1} messages."
        )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


async def setup(bot):
    await bot.add_cog(Admin(bot))
