import discord

from discord.ext import commands

import asyncio

import os

import inspect

import time



bot = commands.Bot(command_prefix='x!')

bot.remove_command('help')



@bot.event

async def on_ready():

	print('Bot is ready')

	

@bot.command(pass_context=True, no_pm=True)

@commands.has_permissions(kick_members=True)

async def clean(ctx, amount=100):

    channel = ctx.message.channel

    messages = [ ]

    async for message in bot.logs_from(channel, limit=int(amount) + 1):

        messages.append(message)

    await bot.delete_messages(messages)

    await bot.say(f"{amount} message has been deleted.")

    

@bot.command(pass_context=True, no_pm=True)

async def help(ctx):

	embed = discord.Embed(title="Help section", description="Here are the commands", color=0xFFFF)

	embed.add_field(name="math", value=">math add (number) (number)")

	embed.add_field(name="math", value=">math subtract (number) (number)")

	embed.add_field(name="math", value=">math multiply (number) (number)")

	embed.add_field(name="math", value=">math divide (number) (number)")

	embed.add_field(name="addrole", value=">addrole @mention (role name)")

	embed.add_field(name="removerole", value=">removerole @mention (role name)")

	embed.add_field(name="clean", value=">clean (amount of message)")

	embed.add_field(name="info", value=">info @mention")

	await bot.say(embed=embed)

	

def user_is_me(ctx):

    return ctx.message.author.id == "381562121865003009"

	

@bot.command(name='eval', pass_context=True)

@commands.check(user_is_me)

async def _eval(ctx, *, command):

    res = eval(command)

    if inspect.isawaitable(res):

        await bot.say(await res)

    else:

        await bot.delete_message(ctx.message)

        await bot.say(res)

        

@_eval.error

async def eval_error(error, ctx):

    if isinstance(error, discord.ext.commands.errors.CheckFailure):

        text = "Sorry {}, You can't use this command only the bot owner can do this.".format(ctx.message.author.mention)

        await bot.send_message(ctx.message.channel, text)

    

@bot.command(pass_context=True)

@commands.has_permissions(kick_members=True)

async def addrole(ctx, user: discord.Member = None, *, name = None):

    author = ctx.message.author

    role = discord.utils.get(ctx.message.server.roles, name=name)

    await bot.add_roles(user, role)

    await bot.say(f'{author.mention} I have added the role {role.mention} to a user {user.mention}'.format(role.name))



@bot.command(pass_context=True)

@commands.has_permissions(kick_members=True)

async def removerole(ctx, user: discord.Member = None, *, name = None):

    author = ctx.message.author

    role = discord.utils.get(ctx.message.server.roles, name=name)

    await bot.remove_roles(user, role)

    await bot.say(f'{author.mention} I have removed the role {role.mention} from a user {user.mention}'.format(role.name))

    

@bot.command(pass_context=True)

async def rename(ctx, name):

	await bot.user.edit(username=name)

    

@bot.command(pass_context=True, no_pm=True)

async def say(ctx, *args):

	mesg = ' '.join(args)

	await bot.delete_message(ctx.message)

	return await bot.say(mesg)

	

@bot.command(pass_context=True, no_pm=True)

async def info(ctx, user: discord.Member):

    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x00ff00)

    embed.add_field(name="Name", value=user.name, inline=True)

    embed.add_field(name="ID", value=user.id, inline=True)

    embed.add_field(name="Status", value=user.status, inline=True)

    embed.add_field(name="Highest role", value=user.top_role)

    embed.add_field(name="Joined", value=user.joined_at)

    embed.set_thumbnail(url=user.avatar_url)

    await bot.say(embed=embed)

    

@bot.command(no_pm=True, hidden=True)

async def servers():

  servers = list(bot.servers)

  await bot.say(f"Connected on {str(len(servers))} servers:")

  await bot.say('\n'.join(server.name for server in servers))

	

@bot.command(pass_context=True)

async def ping(ctx):

    """Pings the bot and gets a response time."""

    pingtime = time.time()

    pingms = await bot.say("Pinging...")

    ping = (time.time() - pingtime) * 1000

    await bot.edit_message(pingms, "Pong! 🏓 ping time is `%dms`" % ping)



@bot.group()

async def math():

    pass

    

@math.command(pass_context=True, no_pm=True)

async def add(ctx, a: int, b:int):

	await bot.say("{} + {} = {}".format(a, b, a+b))

	

@math.command(pass_context=True, no_pm=True)

async def subtract(ctx, a: int, b:int):

	await bot.say("{} - {} = {}".format(a, b, a-b))

	

@math.command(pass_context=True, no_pm=True)

async def multiply(ctx, a: int, b:int):

	await bot.say("{} x {} = {}".format(a, b, a*b))

	

@math.command(pass_context=True, no_pm=True)

async def divide(ctx, a: int, b:int):

	await bot.say("{} ÷ {} = {}".format(a, b, a/b))



bot.run(os.environ['BOT_VALUE'])
