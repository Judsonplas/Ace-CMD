from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx, command_name=None):
        if command_name:
            command = self.bot.get_command(command_name)
            if command is None:
                return await ctx.send("Command not found.")
            return await self.send_command_help(ctx, command)

        categories = {}
        for command in self.bot.commands:
            if command.hidden or command.name == "help":
                continue
            categories.setdefault(command.cog_name or "Other", []).append(command)

        lines = ["Ace-CMD Help"]
        for category, items in sorted(categories.items()):
            lines.append(f"\n{category}")
            for command in sorted(items, key=lambda x: x.name):
                lines.append(f"{ctx.prefix}{command.name}")

        await ctx.send("```\n" + "\n".join(lines)[:1900] + "\n```")

    async def send_command_help(self, ctx, command):
        if hasattr(command, "commands") and command.commands:
            lines = [f"{ctx.prefix}{command.name}"]
            for sub in command.commands:
                lines.append(f"{ctx.prefix}{command.name} {sub.name}")
            return await ctx.send("```\n" + "\n".join(lines) + "\n```")

        usage = command.help or "No usage information available."
        await ctx.send(f"{ctx.prefix}{command.name}\n{usage}")


async def setup(bot):
    await bot.add_cog(Help(bot))
