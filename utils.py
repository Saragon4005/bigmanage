import discord
from discord.ext import commands


def getMessage(ctx: commands.Context):
	'''
	Takes in a context object and outputs the message after the arguments defined
	'''
	cmdlen = len(ctx.args) - 1
	output = []
	for a, i in enumerate(ctx.message.content.split(" ")):
		if i or a > cmdlen:
			if a > cmdlen:
				output.append(i)
		else:
			cmdlen += 1
	return (" ".join(output))
