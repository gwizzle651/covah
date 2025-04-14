import discord
from discord.ext import commands
import os
import random

token = os.getenv("covahBotToken")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

#events
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to discord")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
        
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("🚫 Invalid argument type! Please enter a valid number.")
        
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("⚠️ You are missing some required arguments!")
        
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "lol":
        await message.channel.send("i know that it is not that funny")

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
    await member.dm_channel.send(f'Hello, {member.name}. Welcome to the Server in Discord. Get in an arguement and have some fun!')
    
#commands
@bot.command(name='ping', help='Checks to see if the bot is online.')
async def ping(ctx):
    await ctx.reply("pong")

@bot.command(name='dice', help='Rolls a die between 1 and a given number up to 10 times.')
async def dice(ctx, sides: int, numDice: int):
    rolls = []
    if numDice < 11 and numDice > 0:
        for i in range(numDice):
            rolls.append(str(random.randint(1, sides)))
        await ctx.send(', '.join(rolls))

@bot.command(name='secret')
@commands.has_role('Admin')
async def secret(ctx):
    await ctx.send(f'{ctx.author.name} activated the secret command!')

bot.run(token)
