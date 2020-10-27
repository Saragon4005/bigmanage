import getpass
import utils
import glob, json
import time

import discord
import logger
from discord.ext import commands

from SKCY11X import fileio as SKCYfileio

print("BIGMANAGE BOT B20201026.1")  # X means borked, B is beta, R is release

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
async def write(ctx: commands.Context, channel):
	channel = await bot.fetch_channel(channel.strip("<#>"))
	if ctx.guild == channel.guild:
		await channel.send(utils.getMessage(ctx))
	else:
		raise UnboundLocalError("Refrenced a channel outsite of the scope of the current guild")


@bot.command(name="edit", help="(channel, msg_id, message) Edits a specified message, must be Admin to use.")
@commands.has_permissions(administrator=True)
async def edit(ctx: commands.Context, channel, msg_id):
	channel = await bot.fetch_channel(channel.strip("<#>"))
	if ctx.guild == channel.guild:
		msg_id: discord.Message = await channel.fetch_message(msg_id)
		await msg_id.edit(content=utils.getMessage(ctx))
	else:
		raise UnboundLocalError("Refrenced a channel outsite of the scope of the current guild")


@bot.command(name="mkgroup", help="(*name) makes new channel group(s), must be Admin to use.")
@commands.has_permissions(administrator=True)
async def mkgroup(ctx: commands.Context, *groupname):  # this is beta dont use it
	for i in groupname:
		rootdatabase[ctx.guild]["channelGroups"][i] = []


@bot.event
async def on_ready():
	print(f"{bot.user} is connected to Discord \nWith {bot.command_prefix} as prefix \nCan be mentioned with <@!{bot.user.id}>")


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
		print("Could not process commands \nThis is could be due to bot not being started \nThis is normal for testing")


@bot.event
async def on_error(event, *args, **kwargs):
	with open('err.log', 'a') as f:
		if event == 'on_message':
			f.write(f'Unhandled message: {args[0]}\n')


@bot.event
async def on_command_error(ctx: commands.Context, error):
	await ctx.send(error, delete_after=5)
	print(error)
	raise (error.with_traceback)


def recursivelyRetryStartup(depth):  # this will allow password retries
	if depth > 0:
		TOKENFILE = SKCYfileio(".bot_token", getpass.getpass())
		try:
			return TOKENFILE.read().decode("utf8")
		except ValueError:
			time.sleep(5)
			print(f"\033[91mINCORRECT PASSWORD\033[0m")
			return recursivelyRetryStartup(depth - 1)
	else:  # if password wrong then reject token
		return ""


#print("INIT_DB")
databases = glob.glob("database/*.SKCYDB")
if databases:  # atm this loads any db, fix to load most recent later
	database = SKCYfileio(databases[0], getpass.getpass())
	rootdatabase = json.loads(database.read().decode("utf8"))
else:
	pass
	#	print("BUILD_DB")

print("\033[94mINIT_TOKEN\033[0m")
TOKENFILE_EXISTS = glob.glob(".bot_token")
if not TOKENFILE_EXISTS:  # if tokenfile does not exist then make one
	print("\033[91mTOKEN\033[0m -> \033[94mBUILD_TOKEN\033[0m")
	import BM_GenerateToken
	BM_GenerateToken.gentoken()
	print("\033[92mTOKEN\033[0m -> \033[94mRESUME\033[0m")

try:
	bot.run(recursivelyRetryStartup(3))
except discord.errors.LoginFailure:
	print("\033[91mTOKEN REJECTED\033[0m")
print("\033[94mBOT_EXIT\033[0m")
