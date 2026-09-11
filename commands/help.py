from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx, command_name=None):
        prefix = self.bot.command_prefix

        if command_name:
            command = self.bot.get_command(command_name)
            if not command:
                return await ctx.send("Command not found.")

            await self.send_command_help(ctx, command)
            return

        lines = ["**Ace-CMD Commands**"]
        for command in self.bot.commands:
            if command.hidden:
                continue
            if command.commands:
                lines.append(f"`{prefix}{command.name}` - has subcommands")
            else:
                lines.append(f"`{prefix}{command.name}` - {command.help or 'No description'}")

        await ctx.send("\n".join(lines))

    async def send_command_help(self, ctx, command):
        prefix = self.bot.command_prefix

        if command.commands:
            text = [f"**{prefix}{command.name} commands**"]
            for sub in command.commands:
                text.append(f"`{prefix}{command.name} {sub.name}` - {sub.help or 'No description'}")
            await ctx.send("\n".join(text))
        else:
            await ctx.send(
                f"**{prefix}{command.name}**\n{command.help or 'No description'}"
            )


async def setup(bot):
    await bot.add_cog(Help(bot))
