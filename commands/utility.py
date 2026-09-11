import discord

from discord.ext import commands

from systems.database import (
    get_server_config,
    update_server_config
)

from systems.logger import log_command


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def setup(self, ctx):
        # Creates the server config if it does not exist
        get_server_config(ctx.guild.id)

        msg = "Server configuration created."

        await ctx.send(msg)

        log_command(ctx, msg)


    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild

        msg = (
            f"Server: {guild.name}\n"
            f"ID: {guild.id}\n"
            f"Members: {guild.member_count}\n"
            f"Owner: {guild.owner}"
        )

        await ctx.send(msg)

        log_command(ctx, msg)


    @commands.command()
    async def userinfo(
        self,
        ctx,
        member: discord.Member = None
    ):
        member = member or ctx.author

        msg = (
            f"User: {member.display_name}\n"
            f"ID: {member.id}\n"
            f"Joined: {member.joined_at}"
        )

        await ctx.send(msg)

        log_command(ctx, msg)


    @commands.command()
    async def config(self, ctx):
        config = get_server_config(
            ctx.guild.id
        )

        msg = (
            f"Admin Role: {config.get('admin_role')}\n"
            f"Mod Role: {config.get('mod_role')}\n"
            f"Helper Role: {config.get('helper_role')}\n"
            f"Logs: {config.get('logs')}"
        )

        await ctx.send(msg)

        log_command(ctx, msg)


    @commands.command()
    async def help(self, ctx):
        msg = """
Ace-CMD

Owner:
$status
$say
$dm
$shutdown

Admin:
$lock
$unlock
$slowmode
$clear

Moderation:
$warn
$warnings
$timeout
$kick
$ban

Roles:
$role

AI:
$ai

Utility:
$setup
$serverinfo
$userinfo
$config
"""

        await ctx.send(msg)

        log_command(ctx, msg)


async def setup(bot):
    await bot.add_cog(Utility(bot))
