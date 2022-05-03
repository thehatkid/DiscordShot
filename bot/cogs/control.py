import logging
import asyncio
import aiohttp
import time
import vgamepad
from vgamepad import XUSB_BUTTON
import disnake
from disnake.ext import commands

logger = logging.getLogger(__name__)

# You can put own custom emojis here:
EMOJIS: dict[str, disnake.PartialEmoji] = {
    'empty': disnake.PartialEmoji(name='empty', id=925724134514753576, animated=False),
    'red_up': disnake.PartialEmoji(name='red_up', id=925725083685752882, animated=False),
    'red_down': disnake.PartialEmoji(name='red_down', id=925725083744493578, animated=False),
    'red_left': disnake.PartialEmoji(name='red_left', id=925725083216003114, animated=False),
    'red_right': disnake.PartialEmoji(name='red_right', id=925725083362787358, animated=False),
    'red_a': disnake.PartialEmoji(name='red_a', id=926786983827759115, animated=False),
    'red_b': disnake.PartialEmoji(name='red_b', id=926786984314277928, animated=False),
    'red_x': disnake.PartialEmoji(name='red_x', id=926786984175865921, animated=False),
    'red_y': disnake.PartialEmoji(name='red_y', id=926786984360419348, animated=False)
}


class ViewControls(disnake.ui.View):
    def __init__(self, http: aiohttp.ClientSession, gpad: vgamepad.VX360Gamepad, hold_delay: float = 0.05):
        super().__init__()
        self.timeout = None
        self.http = http
        self.gpad = gpad
        self.hold_delay = hold_delay

    async def on_error(self, error: Exception, item: disnake.ui.Item, ia: disnake.MessageInteraction):
        logger.error(f'Raised exception on view: {error.__class__.__name__}: {error}')
        if isinstance(error, asyncio.exceptions.TimeoutError):
            await ia.send(f'Something goes wrong: `{error.__class__.__name__}: {error}`\nReport to bot author if still not working.', ephemeral=True)

    @disnake.ui.button(emoji=EMOJIS['empty'], style=disnake.ButtonStyle.grey, disabled=True, row=1)
    async def btn_none_1(self, btn: disnake.ui.Button, ia: disnake.MessageInteraction):
        await ia.response.defer()

    @disnake.ui.button(emoji=EMOJIS['red_up'], style=disnake.ButtonStyle.grey, row=1)
    async def btn_move_up(self, btn: disnake.ui.Button, ia: disnake.MessageInteraction):
        await ia.response.defer()
        await self.http.post('/oneshot/lastinputs', json={'author': f'{ia.author}', 'input': 'Up'})
        self.gpad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        self.gpad.update() # Press button DPAD Up
        await asyncio.sleep(self.hold_delay) # Hold button
        self.gpad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        self.gpad.update() # Release button DPAD Up

    @disnake.ui.button(emoji=EMOJIS['empty'], style=disnake.ButtonStyle.grey, disabled=True, row=1)
    async def btn_none_2(self, btn: disnake.ui.Button, ia: disnake.MessageInteraction):
        await ia.response.defer()

    @disnake.ui.button(emoji=EMOJIS['red_left'], style=disnake.ButtonStyle.grey, row=2)
    async def btn_move_left(self, btn: disnake.ui.Button, ia: disnake.MessageInteraction):
        await ia.response.defer()
        await self.http.post('/oneshot/lastinputs', json={'author': f'{ia.author}', 'input': 'Left'})
        self.gpad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        self.gpad.update() # Press button DPAD Left
        await asyncio.sleep(self.hold_delay) # Hold button
        self.gpad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        self.gpad.update() # Release button DPAD Left

    @disnake.ui.button(emoji=EMOJIS['red_down'], style=disnake.ButtonStyle.grey, row=2)
    async def btn_move_down(self, btn: disnake.ui.Button, ia: disnake.MessageInteraction):
        await ia.response.defer()
        await self.http.post('/oneshot/lastinputs', json={'author': f'{ia.author}', 'input': 'Down'})
        self.gpad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        self.gpad.update() # Press button DPAD Down
        await asyncio.sleep(self.hold_delay) # Hold button
        self.gpad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        self.gpad.update() # Release button DPAD Down

    @disnake.ui.button(emoji=EMOJIS['red_right'], style=disnake.ButtonStyle.grey, row=2)
    async def btn_move_right(self, btn: disnake.ui.Button, ia: disnake.MessageInteraction):
        await ia.response.defer()
        await self.http.post('/oneshot/lastinputs', json={'author': f'{ia.author}', 'input': 'Right'})
        self.gpad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        self.gpad.update() # Press button DPAD Right
        await asyncio.sleep(self.hold_delay) # Hold button
        self.gpad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        self.gpad.update() # Release button DPAD Right

    @disnake.ui.button(emoji=EMOJIS['red_a'], label='Action', style=disnake.ButtonStyle.grey, row=3)
    async def btn_action(self, btn: disnake.ui.Button, ia: disnake.MessageInteraction):
        await ia.response.defer()
        await self.http.post('/oneshot/lastinputs', json={'author': f'{ia.author}', 'input': 'Action'})
        self.gpad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gpad.update() # Press button A
        await asyncio.sleep(self.hold_delay) # Hold button
        self.gpad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gpad.update() # Release button A

    @disnake.ui.button(emoji=EMOJIS['red_b'], label='Cancel', style=disnake.ButtonStyle.grey, row=3)
    async def btn_cancel(self, btn: disnake.ui.Button, ia: disnake.MessageInteraction):
        await ia.response.defer()
        await self.http.post('/oneshot/lastinputs', json={'author': f'{ia.author}', 'input': 'Cancel'})
        self.gpad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gpad.update() # Press button B
        await asyncio.sleep(self.hold_delay) # Hold button
        self.gpad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gpad.update() # Release button B

    @disnake.ui.button(emoji=EMOJIS['red_x'], label='Travel', style=disnake.ButtonStyle.grey, row=4)
    async def btn_fasttravel(self, btn: disnake.ui.Button, ia: disnake.MessageInteraction):
        await ia.response.defer()
        await self.http.post('/oneshot/lastinputs', json={'author': f'{ia.author}', 'input': 'Fast Travel'})
        self.gpad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        self.gpad.update() # Press button Left Shoulder
        await asyncio.sleep(self.hold_delay) # Hold button
        self.gpad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        self.gpad.update() # Release button Left Shoulder

    @disnake.ui.button(emoji=EMOJIS['red_y'], label='Items', style=disnake.ButtonStyle.grey, row=4)
    async def btn_items(self, btn: disnake.ui.Button, ia: disnake.MessageInteraction):
        await ia.response.defer()
        await self.http.post('/oneshot/lastinputs', json={'author': f'{ia.author}', 'input': 'Items'})
        self.gpad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
        self.gpad.update() # Press button Y
        await asyncio.sleep(self.hold_delay) # Hold button
        self.gpad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
        self.gpad.update() # Release button Y


class CogControl(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_load(self):
        # Get aiohttp session
        self.http = aiohttp.ClientSession(
            base_url='http://127.0.0.1:8481',
            read_timeout=2,
            loop=self.bot.loop
        )
        # Initialize virtual gamepad
        self.gpad = vgamepad.VX360Gamepad()
        time.sleep(1.5) # wait for sure
        logger.info('Connected virtual gamepad')

    def cog_unload(self):
        # Close aiohttp session
        async def close_http_session():
            await self.http.close()
        self.bot.loop.create_task(close_http_session())
        # "Disconnect" virtual gamepad
        if self.gpad:
            del self.gpad
            time.sleep(1.5) # wait for sure
            logger.info('Disconnected virtual gamepad')

    @commands.command(name='controls', description='Shows a gamepad-like message for controlling OneShot gameplay', aliases=['control', 'ctrl', 'ctl'])
    async def cmd_controls(self, ctx: commands.Context):
        view = ViewControls(self.http, self.gpad, 0.1)
        await ctx.reply('OneShot Controller:tm:', view=view)

    @commands.command(name='message', description='Sends a message box to OneShot', aliases=['msg'])
    @commands.cooldown(1, 60.0, commands.BucketType.user)
    async def cmd_message(self, ctx: commands.Context, face: str = '', *, text: str = ''):
        if not face:
            return await ctx.reply('You forget give a face.\nFor example: `n!message <in-game face> <text>`')

        if not text:
            return await ctx.reply('You forget give a text.\nFor example: `n!message <in-game face> <text>`')

        response = await self.http.post('/oneshot/message', json={'author': f'{ctx.author}', 'face': face, 'text': text})

        if response.status == 404:
            await ctx.reply(f':x: Face `{face}` not exists in game')
            self.cmd_message.reset_cooldown(ctx)
        elif response.status == 409:
            await ctx.reply(f':x: Message was not sent. Try again when no messages boxes')
            self.cmd_message.reset_cooldown(ctx)
        else:
            await ctx.message.add_reaction(u'📤')

    @cmd_message.error
    async def cmd_message_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.reply(f':x: Ayo, please wait {error.retry_after:,.0f} seconds to send again.\nDon\'t be spammy lol')
        else:
            await ctx.reply(f':x: Something went wrong: `{error.__class__.__name__}: {error}`\nReport to bot author if still not working')


def setup(bot: commands.Bot):
    bot.add_cog(CogControl(bot))
    logger.info('Loaded')


def teardown(bot: commands.Bot):
    logger.info('Unloaded')
