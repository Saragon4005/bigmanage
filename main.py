# import atexit

import getpass
import discord

import logger
from discord.ext import commands

from SKCY11X import fileio as SKCYfileio

print("BIGMANAGE BOT X20201014")  # X means borked, B is beta, R is release

print("INIT_TOKEN")
TOKENFILE = SKCYfileio(".bot_token", getpass.getpass())
TOKEN = TOKENFILE.read().decode("utf8")
TOKENFILE.close()

logger.start()

# initialize discord bot
bot = commands.Bot(command_prefix='%', description='', case_insensitive=True)

bot.run(TOKEN)


@bot.command(name="test", help="Responds with 'works!'")
async def test(ctx: commands.Context):
	print('test triggered!')
	await ctx.send("works!")


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


'''
def exit_handler():
    # exit stuff


atexit.register(exit_handler)
'''
