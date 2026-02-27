# Nicolas
# Mariana Bot (Multi Purpose)
# Created: 12-27-2021
# Last Updated: 12-28-2021

# Invite Link: 

import time
import requests # For API calls
import os # For storing data locally
import datetime # For logging time in console

# General discord imports
import discord
from discord.ext import commands
from discord.utils import get


# Hardcoded path to Whitelist.txt
WHITELISTPATH = "C:\\Users\\nsep1\\Desktop\\Projects\\Mariana Bot\\Resources\\Whitelist.txt" 
LOGPATH = "C:\\Users\\nsep1\\Desktop\\Projects\\Mariana Bot\\Resources\\Logs\\"
CHATLOGPATH = "C:\\Users\\nsep1\\Desktop\\Projects\\Mariana Bot\\Resources\\Chat Logs\\"


# Determines whether a user is whitelisted
def Whitelisted(user) -> bool:

    with open(WHITELISTPATH, 'r') as file:
        WHITELIST = [line.strip('\n') for line in file] # Sets WHITELIST to lines of Whitelist.txt

    return (True if user in WHITELIST else False)


def CurrentTime() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")

def UpdateLogFile(line):
    with open(LOGPATH + currentDate + ".txt", 'a') as logfile:
        logfile.write(line + '\n')


###>>> SETUP <<<###

# CREATE OR APPEND TO CURRENT DATE'S LOG FILE
currentDate = datetime.date.today().strftime("%B %d, %Y")
LOGFILEPATH = LOGPATH + currentDate + ".txt"
if os.path.exists(LOGFILEPATH):
    logFile = open(LOGFILEPATH, 'a') # Opens in append mode
else:
    logFile = open(LOGFILEPATH, 'w') # Creates it if it doesn't exist

# Declaring intents
intents = discord.Intents.default()
intents.members = True

# Set command prefix
TOKEN = ''
client = commands.Bot(command_prefix = ">", intents=intents)

zoo = 0
bottesting = 0

client.channel_id = None





###>>> COMMANDS <<<###

# Sends a random fact
@client.command()
async def fact(ctx):
    await ctx.send(requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()['text'])


# Counts messages from a user in a channel
# WHITELIST ENABLED
@client.command()
async def count(ctx, messageAuthor):
    if Whitelisted(str(ctx.message.author)): # Checks to see if command caller is whitelisted
        messageCount = 0
        await ctx.send(f"Counting `{messageAuthor}`'s messages in `{ctx.channel}`...")

        async for message in ctx.channel.history(limit = None): # loops over all messages in the context's channel
            # Increments messageCount by 1 if the author is the same as the parameter
            if str(message.author) == messageAuthor:
                messageCount += 1
    
        await ctx.send(f"`{messageAuthor}` has sent `{messageCount}` messages in `{ctx.channel}`")


# Deletes all of a given user's messages
# WHITELIST ENABLED
@client.command()
async def prune(ctx, messageAuthor, lim = 10):
    author = str(ctx.message.author)

    if Whitelisted(author): # Checks to see if command caller is whitelisted
        async for message in ctx.channel.history(limit = lim): # loop over history
            if author == messageAuthor:
                await message.delete() # delete every stated user's messages in context channel

        output = f"[{CurrentTime()}] {author} deleted {lim} of {messageAuthor}'s messages in {ctx.channel}"

        print(output)
        UpdateLogFile(output)


@client.command()
async def void(ctx):
    async for message in ctx.channel.history(limit = None):
        await message.delete()


# Adds / Removes users from the Whitelist
@client.command()
async def whitelist(ctx, username, type = "add"):
    author = str(ctx.message.author)
    ran = False

    if Whitelisted(author):

        # Read the lines from Whitelist.txt, remove all newlines
        with open(WHITELISTPATH, 'r') as file:
            whitelist = [line.strip('\n') for line in file.readlines()] 
    
        # If parameter is add and user isn't in the whitelist, add them
        if ((type == "add") and (username not in whitelist)):
            whitelist.append(username)
            ran = True
            output = f"[{CurrentTime()}] {author} added {username} to the Whitelist"

            print(output) # Log in console
            UpdateLogFile(output)
            
        
        # If parameter is remove and user is in the whitelist, remove them
        elif ((type == "remove") and (username in whitelist)):
            whitelist.remove(username)
            ran = True
            output = f"[{CurrentTime()}] {author} removed {username} from the Whitelist"

            print(output) # Log in console
            UpdateLogFile(output)
            
        # Update Whitelist.txt
        if (ran): # Checks if either previous if statements have run
            with open(WHITELISTPATH, 'w') as file:
                for entry in whitelist:
                    file.write(entry + '\n')


# Sets the window to a channel
@client.command()
async def window(ctx, Channel=None):
    author = str(ctx.message.author)
    if Whitelisted(author):
        # Check if the channel is set, if not then default to the channel the command was sent in
        if Channel != None:
            channel = discord.utils.get(client.get_guild(bottesting).text_channels, name=Channel)
            print(f"[{CurrentTime()}] {author} has set the view to {Channel}")
        else:
            channel = ctx.channel
        # Set channel_id to the channel id
        client.channel_id = channel.id


# Logs an entire channel's chat history
@client.command()
async def log(ctx, channel):
    channel = discord.utils.get(client.get_guild(bottesting).text_channels, name=channel) # get channel object
    path = CHATLOGPATH + currentDate + ".txt"; filename = currentDate + ".txt"
    count = 0; start = CurrentTime()

    if os.path.exists(path):
        chatlogfile = open(path, 'a') # open or create the file in append mode
    else:
        chatlogfile = open(path, 'w')

    async for message in channel.history(limit = None, oldest_first = True): # get messages, oldest first
        try:
            print(f"[{start}] Logging messages ({count})", end="\r")
            chatlogfile.write(f'[{message.created_at}], {message.author}: {message.content}' + '\n') # write the messages into the file
            count += 1
        except:
            pass
    print("") # Breaks out of the carriage return

    output = f"[{CurrentTime()}] {ctx.message.author} has logged {channel}'s chat history into '{filename}'"

    print(output)
    UpdateLogFile(output) # Log the event


@client.command()
async def play(ctx):
    voice_channel = ctx.author.channel
    if voice_channel != None:
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="C:/Users/nsep1/Desktop/file.wav"))
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()
    else:
        pass



###>>> EVENTS <<<###

# ON_READY()
@client.event
async def on_ready():
    print(f"[{CurrentTime()}] MarianaBot is online\n")


@client.event
async def on_message(message):

     #Check if the message is in the channel set by view()
    if message.channel.id == client.channel_id and message.channel.id != None:

        print(f"[{CurrentTime()}] {message.author}: {message.content}")
    await client.process_commands(message)

# Start

client.run(TOKEN)

