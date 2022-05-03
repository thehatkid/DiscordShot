import logging
import yaml
import disnake
from disnake.ext import commands

# Setting up Logging
logging.basicConfig(
    format='[%(asctime)s][%(levelname)s][%(name)s]: %(message)s',
    level=logging.INFO
)
log = logging.getLogger('bot')

# Loading configurations
cfg = yaml.safe_load(open('config.yml', 'r'))

log.info('Starting disnake {0} {1}...'.format(
    disnake.__version__, disnake.version_info.releaselevel
))

# Initialize Gateway Intents
intents = disnake.Intents(
    guilds=True,
    dm_messages=True,
    guild_messages=True
)

# Initialize Bot Class
bot = commands.Bot(
    command_prefix=cfg['bot']['prefix'],
    help_command=None,
    intents=intents,
    allowed_mentions=disnake.AllowedMentions(
        everyone=False,
        users=True,
        roles=False,
        replied_user=False
    ),
    activity=disnake.Game(name='OneShot'),
    status=disnake.Status.online
)

# Loading Cogs
bot.load_extension('cogs.events')
bot.load_extension('cogs.commands')
bot.load_extension('cogs.control')

# Running Bot from Bot Token
bot.run(token=cfg['bot']['token'])
