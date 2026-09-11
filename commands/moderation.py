import discord

from datetime import timedelta

from discord.ext import commands

from systems.database import (
    get_server_config,
    add_warning,
    get_user_warnings
)

from systems.permissions import (
    is_mod,
    is_helper
)

from systems.logger import log_command


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def warn(
        self,
        ctx,
        member: discord.Member,
        *,
        reason="No reason provided"
    ):
        config = get_server_config(
            ctx.guild.id
        )

        if not is_helper(ctx.author, config):
            return await ctx.send(
                "No permission."
            )


        warning = {
            "reason": reason,
            "moderator": ctx.author.id
        }


        add_warning(
            ctx.guild.id,
            member.id,
            warning
        )


        msg = (
            f"{member.display_name} warned.\n"
            f"Reason: {reason}"
        )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @commands.command()
    async def warnings(
        self,
        ctx,
        member: discord.Member
    ):
        warnings = get_user_warnings(
            ctx.guild.id,
            member.id
        )


        if not warnings:
            msg = (
                f"{member.display_name} "
                "has no warnings."
            )

        else:
            msg = (
                f"{member.display_name} warnings:\n"
                f"{warnings}"
            )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @commands.command()
    async def timeout(
        self,
        ctx,
        member: discord.Member,
        minutes: int = 10
    ):
        config = get_server_config(
            ctx.guild.id
        )

        if not is_mod(ctx.author, config):
            return await ctx.send(
                "No permission."
            )


        await member.timeout(
            timedelta(minutes=minutes)
        )


        msg = (
            f"{member.display_name} "
            f"timed out for {minutes} minutes."
        )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @commands.command()
    async def kick(
        self,
        ctx,
        member: discord.Member,
        *,
        reason="No reason provided"
    ):
        config = get_server_config(
            ctx.guild.id
        )

        if not is_mod(ctx.author, config):
            return await ctx.send(
                "No permission."
            )


        await member.kick(
            reason=reason
        )


        msg = (
            f"{member.display_name} kicked.\n"
            f"Reason: {reason}"
        )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @commands.command()
    async def ban(
        self,
        ctx,
        member: discord.Member,
        *,
        reason="No reason provided"
    ):
        config = get_server_config(
            ctx.guild.id
        )

        if not is_mod(ctx.author, config):
            return await ctx.send(
                "No permission."
            )


        await member.ban(
            reason=reason
        )


        msg = (
            f"{member.display_name} banned.\n"
            f"Reason: {reason}"
        )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


async def setup(bot):
    await bot.add_cog(Moderation(bot))
