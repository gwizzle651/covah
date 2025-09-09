import discord
from discord.ext import commands, tasks
import os
import random

token = os.getenv("covahBotToken")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

botCommandsChannelID = 1345050469302665257


# events
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to discord")
    bumpServer.start()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.reply("You don't have permission to use this command.")

    elif isinstance(error, commands.BadArgument):
        await ctx.reply("🚫 Invalid argument(s)!")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("⚠️ You are missing some required argument(s)!")
    elif isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "lol":
        # await message.channel.send("i know that it is not that funny")
        await message.reply('i know that it is not that funny')

    if message.content.lower() == "bruh":
        await message.reply('shut up loser')

    if message.content == "🦐":
        await message.reply('🥐 fr*nch 🥖')
        await message.add_reaction('🇨🇵')
    if message.content == '🧽':
        await message.reply('S P O N G U E')

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hello, {member.name}."
                                 " Welcome to the Server in Discord."
                                 " Get in an arguement and have some fun!")


# commands
@bot.command(name='ping', help='Checks to see if the bot is online.')
async def ping(ctx):
    await ctx.reply("pong")


@bot.command(name="dice", help="Rolls a die between 1 and"
             " a given number up to 10 times.")
async def dice(ctx, sides: int, numDice: int):
    rolls = []
    if numDice < 11 and numDice > 0:
        for i in range(numDice):
            rolls.append(str(random.randint(1, sides)))
        await ctx.send(', '.join(rolls))


@bot.command(name='secret', help='Completely useless.')
@commands.has_role('Admin')
async def secret(ctx):
    await ctx.send(f'{ctx.author.name} activated the secret command!')

'''
@bot.command(name='strike', help='Manages the striking system.')
@commands.has_any_role('Admin', 'Mod')
async def strike(ctx, mode: str, user: discord.Member, *, reason=None):
    if mode not in ['add', 'remove']:
        await ctx.send("Invalid mode. Use 'add' to issue a strike or"
                       " 'remove' to remove a strike.")
        return

    if user.id not in user_strikes:
        user_strikes[user.id] = 0
    if mode == 'add':
        user_strikes[user.id] += 1
        await ctx.send(f"Strike added to {user.name}."
                       "Total strikes: {user_strikes[user.id]}")

        if user_strikes[user.id] >= 3:
            await ctx.send(f"{user.name} has reached 3 strikes and"
                           " will be muted by @Admin or @Mod.")

    elif mode == 'remove':
        if user_strikes[user.id] > 0:
            user_strikes[user.id] -= 1
            await ctx.send(f"Strike removed from {user.name}."
                           " Total strikes: {user_strikes[user.id]}")
        else:
            await ctx.send(f"{user.name} has no strikes to remove.")

    if reason:
        await ctx.send(f"Reason: {reason}")
'''


# automation
@tasks.loop(hours=1)
async def bumpServer():
    await bot.wait_until_ready()
    channel = bot.get_channel(botCommandsChannelID)
    if channel:
        await channel.send("<@&1414763923780927568>"
                           "It's time to bum the server.")
    else:
        print("Channel not found.")
bot.run(token)
