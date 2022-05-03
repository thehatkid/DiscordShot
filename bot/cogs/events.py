import logging
import sys
import traceback
import disnake
from disnake.ext import commands

logger = logging.getLogger(__name__)


class CogEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Bot is Ready as {}'.format(self.bot.user))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        logger.info('Bot has been invited to: [Name: {0}, ID: {1}]'.format(guild.name, guild.id))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: disnake.Guild):
        logger.info('Bot has been kicked from: [Name: {0}, ID: {1}]'.format(guild.name, guild.id))

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.errors.MissingRequiredArgument):
            await ctx.reply(f':x: Required Argument: `{exception.param}`')
        elif isinstance(exception, commands.errors.CheckFailure):
            await ctx.reply(':x: You don\'t have access to this command')
        elif isinstance(exception, commands.errors.BadArgument):
            await ctx.reply(f':x: Bad Argument: `{exception}`')
        elif isinstance(exception, commands.CommandOnCooldown):
            pass
        elif isinstance(exception, commands.CommandNotFound):
            pass
        else:
            logger.error(f'Raised exception on executing command "{ctx.command.name}"!')
            traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)


def setup(bot: commands.Bot):
    bot.add_cog(CogEvents(bot))
    logger.info('Loaded')


def teardown(bot: commands.Bot):
    logger.info('Unloaded')
