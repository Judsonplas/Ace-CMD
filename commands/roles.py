import discord

from discord.ext import commands

from systems.database import get_server_config, update_server_config
from systems.permissions import is_admin
from systems.logger import log_command


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def role(self, ctx):
        await ctx.send(
            "Role help:\n"
            "$role set admin <role_id>\n"
            "$role set mod <role_id>\n"
            "$role set helper <role_id>\n"
            "$role list\n"
            "$role give @user <role_id>\n"
            "$role remove @user <role_id>"
        )

    @role.command()
    async def set(self, ctx, role_type: str, role_id: int):
        config = get_server_config(ctx.guild.id)
        if not is_admin(ctx.author, config):
            return await ctx.send("No permission.")

        if role_type not in ["admin", "mod", "helper"]:
            return await ctx.send("Invalid role type.")

        update_server_config(ctx.guild.id, f"{role_type}_role", role_id)
        await ctx.send(f"{role_type} role set to {role_id}")

    @role.command(name="list")
    async def list_roles(self, ctx):
        config = get_server_config(ctx.guild.id)
        await ctx.send(
            f"Admin: {config.get('admin_role')}\n"
            f"Mod: {config.get('mod_role')}\n"
            f"Helper: {config.get('helper_role')}"
        )

    @role.command()
    async def give(self, ctx, member: discord.Member, role_id: int):
        config = get_server_config(ctx.guild.id)
        if not is_admin(ctx.author, config):
            return await ctx.send("No permission.")

        role = ctx.guild.get_role(role_id)
        if role is None:
            return await ctx.send("Role not found.")

        await member.add_roles(role)
        await ctx.send(f"Gave {role.name} to {member.display_name}")

    @role.command()
    async def remove(self, ctx, member: discord.Member, role_id: int):
        config = get_server_config(ctx.guild.id)
        if not is_admin(ctx.author, config):
            return await ctx.send("No permission.")

        role = ctx.guild.get_role(role_id)
        if role is None:
            return await ctx.send("Role not found.")

        await member.remove_roles(role)
        await ctx.send(f"Removed {role.name} from {member.display_name}")


async def setup(bot):
    await bot.add_cog(Roles(bot))
