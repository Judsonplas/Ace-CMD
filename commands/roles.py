import discord

from discord.ext import commands

from systems.database import (
    get_server_config,
    update_server_config
)

from systems.permissions import is_admin

from systems.logger import log_command


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(
        invoke_without_command=True
    )
    async def role(self, ctx):
        msg = (
            "Role commands:\n"
            "$role set admin <role_id>\n"
            "$role set mod <role_id>\n"
            "$role set helper <role_id>\n"
            "$role list\n"
            "$role give @user <role_id>"
        )

        await ctx.send(msg)


    @role.command()
    async def set(
        self,
        ctx,
        role_type: str,
        role_id: int
    ):
        config = get_server_config(
            ctx.guild.id
        )

        if not is_admin(ctx.author, config):
            return await ctx.send(
                "No permission."
            )


        if role_type not in [
            "admin",
            "mod",
            "helper"
        ]:
            return await ctx.send(
                "Invalid role type."
            )


        update_server_config(
            ctx.guild.id,
            f"{role_type}_role",
            role_id
        )


        msg = (
            f"{role_type} role set to "
            f"{role_id}"
        )

        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @role.command(name="list")
    async def list_roles(self, ctx):
        config = get_server_config(
            ctx.guild.id
        )

        msg = (
            f"Admin: {config.get('admin_role')}\n"
            f"Mod: {config.get('mod_role')}\n"
            f"Helper: {config.get('helper_role')}"
        )

        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @role.command()
    async def give(
        self,
        ctx,
        member: discord.Member,
        role_id: int
    ):
        config = get_server_config(
            ctx.guild.id
        )

        if not is_admin(ctx.author, config):
            return await ctx.send(
                "No permission."
            )


        role = ctx.guild.get_role(
            role_id
        )

        if role is None:
            return await ctx.send(
                "Role not found."
            )


        await member.add_roles(role)


        msg = (
            f"Gave {role.name} "
            f"to {member.display_name}"
        )

        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


async def setup(bot):
    await bot.add_cog(Roles(bot))
