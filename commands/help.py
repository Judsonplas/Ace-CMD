from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        categories = {}

        for command in self.bot.commands:
            if command.hidden or command.name == "help":
                continue

            cog = command.cog_name or "Other"
            categories.setdefault(cog, []).append(command)

        lines = ["**Ace-CMD Help**"]
        for category, commands_list in categories.items():
            lines.append(f"\n**{category}**")
            for command in commands_list:
                lines.append(f"`{ctx.prefix}{command.name}`")

        await ctx.send("\n".join(lines))


async def setup(bot):
    await bot.add_cog(Help(bot))
