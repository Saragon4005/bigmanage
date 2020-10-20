# import atexit

import getpass
import discord

import logger
from discord.ext import commands

from SKCY11X import fileio as SKCYfileio

print("BIGMANAGE BOT B20201019.0")  # X means borked, B is beta, R is release

logger.start()

intents = discord.Intents(guild_messages=True, guilds=True)
allowedMentions = discord.AllowedMentions(everyone=False, users=False, roles=False)

# initialize discord bot
bot = commands.Bot(command_prefix='%', description='', case_insensitive=True, intents=intents, allowed_mentions=allowedMentions)


@bot.command(name="test", help="Responds with 'works!'")
async def test(ctx: commands.Context):
	print('test triggered!')
	await ctx.send("works!")


@bot.command(name="write", help="Sends a message to the specified channel, must be Admin to use.")
@commands.has_permissions(administrator=True)
async def write(ctx, channel, *message):
	channel = await bot.fetch_channel(channel.strip("<#>"))
	await channel.send(" ".join(message))


@bot.command(name="edit", help="(channel, msg_id, message) Edits a specified message, must be Admin to use.")
@commands.has_permissions(administrator=True)
async def edit(ctx, channel, msg_id, *message):
	channel = await bot.fetch_channel(channel.strip("<#>"))
	msg_id: discord.Message = await channel.fetch_message(msg_id)
	await msg_id.edit(content=" ".join(message))


@bot.event
async def on_ready():
	print(f'{bot.user} is connected to Discord\n' f'With {bot.command_prefix} as prefix\n' f"Can be mentioned with <@!{bot.user.id}>")


@bot.event
async def on_connect():
	print("Connected!")


'''
@bot.event
async def on_member_join(member: discord.Member):
    # only work in the test guild
    if(member.guild.id == 660979844179427368):
        # set announcements as current channel
        channel = bot.get_channel(660987946085646367)
        await channel.send(f'Welcome {member.name}!')
'''


@bot.event
async def on_message(message: discord.Message):
	if message.author == bot.user:
		return 0
	try:
		await bot.process_commands(message)
	except AttributeError:
		print("Could not process commands \n" "This is could be due to bot not being started \n" "This is normal for testing")


@bot.event
async def on_error(event, *args, **kwargs):
	with open('err.log', 'a') as f:
		if event == 'on_message':
			f.write(f'Unhandled message: {args[0]}\n')


@bot.event
async def on_command_error(ctx, error):
	await ctx.send(error)
	print(error)
	raise (error.with_traceback)


'''
def exit_handler():
    # exit stuff


atexit.register(exit_handler)
'''

print("INIT_TOKEN")
TOKENFILE = SKCYfileio(".bot_token", getpass.getpass())
bot.run(TOKENFILE.read().decode("utf8"))
TOKENFILE.close()
