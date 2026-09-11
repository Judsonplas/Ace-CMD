import discord

from discord.ext import commands

from systems.permissions import is_owner
from systems.logger import log_command


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def status(
        self,
        ctx,
        *,
        text
    ):
        if not is_owner(ctx.author):
            return await ctx.send(
                "Owner only."
            )


        await self.bot.change_presence(
            activity=discord.Game(text)
        )


        msg = (
            f"Status changed to: {text}"
        )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @commands.command()
    async def say(
        self,
        ctx,
        channel: discord.TextChannel,
        *,
        message
    ):
        if not is_owner(ctx.author):
            return await ctx.send(
                "Owner only."
            )


        await channel.send(
            message
        )


        msg = (
            f"Sent message in "
            f"{channel.name}"
        )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @commands.command()
    async def dm(
        self,
        ctx,
        user: discord.User,
        *,
        message
    ):
        if not is_owner(ctx.author):
            return await ctx.send(
                "Owner only."
            )


        await user.send(
            message
        )


        msg = (
            f"DM sent to "
            f"{user.display_name}"
        )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


    @commands.command()
    async def shutdown(self, ctx):
        if not is_owner(ctx.author):
            return await ctx.send(
                "Owner only."
            )


        msg = "Bot shutting down."

        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )

        await self.bot.close()


    @commands.command()
    async def reload(
        self,
        ctx,
        extension
    ):
        if not is_owner(ctx.author):
            return await ctx.send(
                "Owner only."
            )


        try:
            await self.bot.reload_extension(
                f"commands.{extension}"
            )

            msg = (
                f"Reloaded {extension}"
            )

        except Exception as e:
            msg = (
                f"Reload failed:\n{e}"
            )


        await ctx.send(msg)

        log_command(
            ctx,
            msg
        )


async def setup(bot):
    await bot.add_cog(Owner(bot))
