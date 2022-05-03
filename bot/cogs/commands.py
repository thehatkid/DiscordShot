import logging
from disnake.ext import commands

logger = logging.getLogger(__name__)


class CogCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='reload', description='Reloads a cog without restarting bot', hidden=True)
    @commands.is_owner()
    async def cmd_reload(self, ctx: commands.Context, which: str = ''):
        if not which:
            return await ctx.reply('Which reload?\n`all`, `events`, `commands` or `control`')

        if which == 'all':
            self.bot.reload_extension('cogs.events')
            self.bot.reload_extension('cogs.commands')
            self.bot.reload_extension('cogs.control')
        elif which == 'events':
            self.bot.reload_extension('cogs.events')
        elif which == 'commands':
            self.bot.reload_extension('cogs.commands')
        elif which == 'control':
            self.bot.reload_extension('cogs.control')

        await ctx.reply(':arrows_counterclockwise: Reloaded cog: `{}`'.format(which))


def setup(bot: commands.Bot):
    bot.add_cog(CogCommands(bot))
    logger.info('Loaded')


def teardown(bot: commands.Bot):
    logger.info('Unloaded')
