import discord
from discord.ext import commands, tasks
import os
import random
import json

token = os.getenv("covahBotToken")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)


def loadStrikes():
    try:
        with open('userStrikes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def saveStrikes():
    with open('userStrikes.json', 'w') as f:
        json.dump(userStrikes, f)


actionLogChannelID = 1252706858192474174
botCommandsChannelID = 1345050469302665257
userStrikes = loadStrikes()


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
        await ctx.send("An error occurred for an unknown reason.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "lol" in message.content.lower():
        await message.reply("i know that it is not that funny")

    if "bruh" in message.content.lower():
        await message.reply("shut up loser")

    if "🧽" in message.content:
        await message.reply("S P O N G U E")

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
    await ctx.send(f"{ctx.author.name} activated the secret command!")


@bot.command(name="clear", help="Clears a specified number of messages."
             " from the channel it is called in.")
@commands.has_any_role("Admin", "Mod")
async def clear(ctx, amount: int):
    if amount < 101:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Cleared {amount} messages.")
    else:
        await ctx.send("You can only clear up to 100 messages at a time.")


# make sure to edit the rulesMessage variable to fit server's rules
@bot.command(name='rules', help="Posts the server rules"
             " in the current channel.")
async def rules(ctx):
    rulesMessage = (
        "1. Don't spam. (This includes reactions & forum posts)\n"
        "2. No NSFW content. (Or otherwise inappropriate content.)\n"
        "3. Stay on topic within specific channels.\n"
        "4. Contact admins if someone is breaking the rules.\n"
        "5. Keep vulgar language to a minimum.\n"
        "6. Be honourable, and remember what happens to your reputation"
        " when you aren't.\n"
        "7. Use English as your primary language. (Other languages"
        " are allowed, just don't use them all the time.)\n"
        "8. Don't try to force anyone to touch gr*ss, get a j*b,"
        " or take a sh*wer/b*th.\n"
        "9. No advertising other websites, discord servers, products,"
        " or any other form of service, object or similar"
        " except for in the dedicated channel.\n"
        "10. No “brainrot” content is allowed. (Except for the one emoji:"
        " :onlyinohio: and chill guy)\n"
        "11. Do not post PII of others. (Unless given explicit"
        " permission by that person.)\n"
        "12. Do not ping everyone (except for mods obv) and only use"
        " role pings when appropriate."
    )
    await ctx.send(rulesMessage)


@bot.command(name="strike", help="Manages the striking system.")
@commands.has_any_role("Admin", "Mod")
async def strike(ctx, mode: str, user: discord.Member, *, reason=None):
    if mode not in ["add", "remove"]:
        await ctx.send("Invalid mode. Use 'add' to issue a strike or"
                       " 'remove' to remove a strike.")
        return

    if user.id not in userStrikes:
        userStrikes[user.id] = 0
    if mode == 'add':
        userStrikes[user.id] += 1
        await ctx.send(f"Strike added to {user.name}."
                       "Total strikes: {userStrikes[user.id]}")

        if userStrikes[user.id] >= 3:
            await ctx.send(f"{user.name} has reached {userStrikes[user.id]}"
                           " strikes and will be punished by"
                           " <@&1252708314157023303> or"
                           " <@&1252703138809380874> accordingly.")

    elif mode == 'remove':
        if userStrikes[user.id] > 0:
            userStrikes[user.id] -= 1
            await ctx.send(f"Strike removed from {user.name}."
                           " Total strikes: {userStrikes[user.id]}")
        else:
            await ctx.send(f"{user.name} has no strikes to remove.")

    if reason:
        channel = bot.get_channel(actionLogChannelID)
        await channel.send(f"Reason: {reason}")
        await ctx.send(f"Reason: {reason}")


# automation
@tasks.loop(hours=2)
async def bumpServer():
    await bot.wait_until_ready()
    channel = bot.get_channel(botCommandsChannelID)
    if channel:
        await channel.send("<@&1414763923780927568>"
                           " It's time to bump the server.")
    else:
        print(f"Channel not found: {botCommandsChannelID}")
bot.run(token)
