#Imports a bunch of stuff
import discord
from discord.ext.commands import *
import logging
from discord.ext import *
from discord.ext import tasks
import asyncio
from discord import *
from discord.ext.commands import *
from badwords import *
import subprocess
import json
import requests
import praw
import random
from ctypes import *
from discord import FFmpegPCMAudio
from discord.utils import get
import os
import sys
#import nltk
#from nltk.stem.lancaster import LancasterStemmer
import random
import json
import pickle
#import numpy
#import tflearn
#from tensorflow.python.compiler.tensorrt import trt_convert as trt
from itertools import cycle
from discord_webhook import DiscordWebhook 


#Gets the server prefixes from prefixes.json
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    try:
        return prefixes[str(message.guild.id)]

    except KeyError:
        with open("prefixes.json", "w") as w:
            prefixes[str(message.guild.id)] = "."
            json.dump(prefixes, w)

client = commands.Bot(command_prefix = get_prefix)


#loads opus
try:
    discord.opus.load_opus("/usr/lib/arm-linux-gnueabihf/libopus.so.0") # Edit the path here
except:
    print("Could not load opus, please edit the opus varibale in the code to the path Opus is in.")


#This is for the reddit command
reddit = praw.Reddit(client_id='F8RFm2aSyTh7mw',
                 client_secret='b4NL3gp6pw8Kr5MNsZO3FBDv3Cw',
                 user_agent='Tribuntu Discord Bot')


@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "."

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=5)
        print(f"Bot has joined a new server! Server name: {guild}")

    try:
        await guild.create_role(name="orange color", colour=discord.Colour(11027200))
        tribuntu_bot = await guild.fetch_member(int("650529752465276958"))
        role = discord.utils.get(guild.roles, name="orange color")
        await tribuntu_bot.add_roles(role)

    except:
        pass

@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "a") as f:
        prefixes = json.load(f)


    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=5)



        print(f"Bot has left the server: {guild}")


logging.basicConfig(level=logging.INFO)


client.remove_command("help")

@client.event
async def on_message_edit(before, after):
    if before.content == after.content:
        return
    try:
        the_guild = before.guild
        the_channel = discord.utils.get(the_guild.text_channels, name="logs")
        the_author = before.author
        if the_author.bot == True:
            return
        embed = discord.Embed(title="Message Edit", description=f"{the_author} edited a message", color=3447003)
        embed.add_field(name="Before Edit:", value=before.content, inline=False)
        embed.add_field(name="After Edit:", value=after.content, inline=False)
        await the_channel.send(embed=embed)

    except:
        pass
@client.event
async def on_message_delete(message):
    try:
        the_guild = message.guild
        the_channel = discord.utils.get(the_guild.text_channels, name="logs")
        the_author = message.author
        if the_author.bot == True:
            return
        embed = discord.Embed(title="Message Delete", description=f"{the_author} deleted a message", color=15158332)
        embed.add_field(name="Deleted Message:", value=message.content, inline=False)
        await the_channel.send(embed=embed)

    except:
        pass

@client.event
async def on_member_join(member):
    try:
        the_guild = member.guild
        the_channel = discord.utils.get(the_guild.text_channels, name="logs")
        embed = discord.Embed(title="Member Join", description="A new member has joined the server", color=3066993)
        embed.add_field(name="Member:", value=f"{member}", inline=False)
        embed.add_field(name="Member ID", value=f"{member.id}", inline=False)
        await the_channel.send(embed=embed)
    except:
        pass



@client.event
async def on_member_remove(member):
    try:
        the_guild = member.guild
        the_channel = discord.utils.get(the_guild.text_channels, name="logs")
        embed = discord.Embed(title="Member Leave", description="A member has left the server", color=9807270)
        embed.add_field(name="Member:", value=f"{member}", inline=False)
        embed.add_field(name="Member ID", value=f"{member.id}", inline=False)
        await the_channel.send(embed=embed)
    except:
        pass

#@client.event
#async def on_member_update(before, after):
#    if after.bot == True:
#        return
#
#    r = open("disabled_logging.json", "r")
#    contents = json.load(r)
#
#    if after.id in contents:
#            return
#
#    the_guild = after.guild
#
#    if after not in the_guild.members:
#        return
#
#    the_channel = discord.utils.get(the_guild.text_channels, name="tribuntu-logs")
#    try:
#        if before.status != after.status:
#            embed = discord.Embed(title="Status Update", description="A member's status has changed", color= 2123412)
#            embed.add_field(name="Member:", value=f"{after}", inline=False)
#            embed.add_field(name="Old Status:", value=f"{before.status}", inline=False)
#            embed.add_field(name="New Status:", value=f"{after.status}", inline=False)
#            await the_channel.send(embed=embed)
#
#        if before.activity != after.activity:
#            embed = discord.Embed(title="Activity Update", description="A member's activity has changed", color= 2123412)
#            embed.add_field(name="Member:", value=f"{after}", inline=False)
#            embed.add_field(name="Old activity:", value=f"{before.activity.name}", inline=False)
#            embed.add_field(name="New activty:", value=f"{after.activity.name}", inline=False)
#            await the_channel.send(embed=embed)
#
#        if before.nick != after.nick:
#            embed = discord.Embed(title="Nickname Update", description="A member's nickmame has been changed", color= 2123412)
#            embed.add_field(name="Member:", value=f"{after}", inline=False)
#            embed.add_field(name="Old Nickname:", value=f"{before.nick}", inline=False)
#            embed.add_field(name="New Nickname", value=f"{after.nick}", inline=False)
#            await the_channel.send(embed=embed)
#
#    except AttributeError:
#        pass

#Sends memes in channels every 60 seconds
@tasks.loop(seconds=300)
async def send_memes_in_channels():
    try:
        f = open("meme_channels.json", "r")
        c = json.load(f)

        response = requests.get("https://meme-api.herokuapp.com/gimme")
        response = response.json()
        title = response["title"]
        meme = response["url"]
        embed = discord.Embed(title=f"{title}", description=None, color=15105570)
        embed.set_image(url=f"{meme}")
        embed.set_footer(text="Memes are sent every 5 minutes")


        for w in c:
            the_guild_to_send_memes_in = client.get_guild(int(w))
            channel = discord.utils.get(the_guild_to_send_memes_in.text_channels, name="5-minute-memes")
            if not channel:
                with open("meme_channels.json", "r") as s:
                    the_file_contents_list = json.load(s)
                    with open("meme_channels.json", "w") as t:
                        the_file_contents_list.remove(w)
                        json.dump(the_file_contents_list, t)
                        continue
            await channel.send(embed=embed)

    except Exception as error:
        print(error)

@tasks.loop(minutes=1)
async def finished_song_disconnect():
    global music_message_authors
    global play_control_messages
    for x in client.voice_clients:
        if x.is_playing() == False:
            await x.disconnect()
            play_control_message = play_control_messages[str(x.channel.guild.id)]
            await play_control_message.edit(content='''
            Use the reactions to pause/play the music!
    *current status:* **Canceled/Finished**''')
            await play_control_message.clear_reactions()
            try:
                del music_message_authors[str(x.guild.id)]
            except KeyError:
                pass

#When bot starts, this is what it prints
@client.event
async def on_ready():
    print("Bot is online and ready to go!")
    change_status.start()
    guilds = client.guilds
    finished_song_disconnect.start()

    for guild in guilds:
        print(guild.name)

    global all_members_list
    all_members_list = []
    send_memes_in_channels.start()

    for x in client.get_all_members():
        all_members_list.append(x)

    global client_guilds
    client_guilds = []

    for t in client.guilds:
        client_guilds.append(t)

    global status
    status = cycle(["Type '.help' for help", "Offical Support Server: https://discord.gg/6QN8nd6", "Please use the '.feedback' command for feedback", f"in {len(client.guilds)} guilds", f"Watching over {len(all_members_list)} people", "Update: Memes are now scraped from Reddit!"])


#This line of code changes the status and what game the bot is playing.
@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


levelups = open("levelups.json", "r")
f = json.load(levelups)
levelups.close()

@client.event
async def on_disconnect():
    global f
    levels = open("levelups.json", "w")
    json.dump(f, levels)
    levels.close()
    change_status.stop()
    send_memes_in_channels.stop()
    finished_song_disconnect.stop()


#All the commands:


#Stops bots from using commands and level ups
@client.event
async def on_message(message):
    global f
    if message.guild == None:
        if message.author.bot == True:
            return
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/681935465993207848/SFSA1ivP8t-Mva9GqRUKHiOigsQPB7RfH58_Xvvf7t0Tfd2OsnMOflurTkH-Vr3Oqqnl', content=f'''**From:** {message.author}
**User ID:** {message.author.id}
**Content:** {message.content}''')
        webhook.execute()
        return
    message_author = message.author.id
    message_author_name = message.author
    try:
        guild_id = message.guild.id
    except AttributeError:
        return

    with open("disabled_servers.json", "r") as d:
        try:
            disabled_servers = json.load(d)
        except:
            d = open("disabled_servers.json", "w")
            d.write("{}")
            d.close()
            disabled_servers = json.load(d)
        for x in disabled_servers:
            if message.guild.id not in disabled_servers:
                break
            await client.process_commands(message)

            return

        if message.author.bot == True:
            return


        try:
            f[str(message.author.id)] += 1
        except KeyError:
            f[str(message.author.id)] = 1

        if f[str(message_author)] == 50:
            await message.channel.send(f"🎉 {message_author_name.mention}, you leveled up to level 1! Congratulations!")
        if f[str(message_author)] == 100:
            await message.channel.send(f"🎉 {message_author_name.mention}, you leveled up to level 2! Congratulations!")
        if f[str(message_author)] == 150:
            await message.channel.send(f"🎉 {message_author_name.mention}, you leveled up to level 3! Congratulations!")
        if f[str(message_author)] == 200:
            await message.channel.send(f"🎉 {message_author_name.mention}, you leveled up to level 4! Congratulations!")
        if f[str(message_author)] == 250:
            await message.channel.send(f"🎉 {message_author_name.mention}, you leveled up to level 5! Congratulations!")
        if f[str(message_author)] == 300:
            await message.channel.send(f"🎉 {message_author_name.mention}, you leveled up to level 6! Congratulations!")
        if f[str(message_author)] == 350:
            await message.channel.send(f"🎉 {message_author_name.mention}, you leveled up to level 7! Congratulations!")
        if f[str(message_author)] == 400:
            await message.channel.send(f"🎉 {message_author_name.mention}, you leveled up to level 8! Congratulations!")
        if f[str(message_author)] == 450:
            await message.channel.send(f"🎉 {message_author_name.mention}, you leveled up to level 9! Congratulations!")
        if f[str(message_author)] == 500:
            await message.channel.send(f"🎉 **Congratulations {message_author_name.mention}, you have made it to level 10 and sent 500 messages!**")

   #with open("custom_commands.json", "w") as f:
  #     file_contents = json.load(f)
 #      if file_contents[str(f"{command.guild.id}_{message.content}")] in file_contents:
#           await message.channel.send(f"{file_contents[str(f"{message.guild.id}")]}")

    await client.process_commands(message)

#Clear command
@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)
    purge_message = await ctx.send("Messages purged. This message will delete in 3 seconds.")
    await asyncio.sleep(3)
    print(f"The command 'clear' was used in the server: {ctx.guild}")
    await purge_message.delete()

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to clear messages.")
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("You have to tell me how many messages do you want deleted...")

#Kick command
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"**{member} has been kicked.** :white_check_mark:")
    except:
        await ctx.send("This person is an Admin and cannot be banned or kicked. :x:")
    finally:
        print(f"The command 'kick' was used in the server: {ctx.guild}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to kick people.")
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Can you please tell me who to kick?")


#Ban command
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"**{member} has been banned. :white_check_mark: **")
    except:
        await ctx.send("This person is an Admin and cannot be banned or kicked. :x:")
    finally:
        print(f"The command 'ban' was used in the server: {ctx.guild}")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permission to ban people.")
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Can you please tell me who to ban?")

#Ping command
@client.command()
async def ping(ctx):
    if ctx.guild.id == int("471170550924967937"):
        await ctx.guild.leave()
    await ctx.send("Pong! If you need help, use the `.feedback` command to send feedback to the Owner!")
    print(f"The command 'ping' was used in the server: {ctx.guild}")

#Talking though the bot
@client.command()
@has_permissions(administrator=True)
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(msg)
    print(f"{ctx.author} in {ctx.guild} made the bot say \"{msg}\"")


@say.error
async def say_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permission to talk through the bot.")
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("What do you want the bot to say?")


#Clear all messages in a channel
@client.command()
@has_permissions(administrator=True)
async def clearall(ctx):
    await ctx.send("Please note that Discord does not allow bots to remove messages older than 14 days.")
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=99999999)
    sucess_message = await ctx.send("Messages cleared. :white_check_mark:")
    await asyncio.sleep(3)
    await sucess_message.delete()
    print(f"The command 'clearall' was used in the server: {ctx.guild}")

@clearall.error
async def clearall_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to clear all messages in a channel.")

#RickRoll command
@client.command()
async def rickroll(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("**Breaking news! President Donald Trump has been killed! Link below:**")
    await ctx.send("<https://www.youtube.com/watch?v=dQw4w9WgXcQ>")
    print(f"The command 'rickroll' was used in the server: {ctx.guild}")


#Kill command
@client.command()
async def kill(ctx, *, person):
    await ctx.send(f"**{person} gets yeeted off of a cliff by God.**")
    print(f"The command 'kill' was used in the server: {ctx.guild}")


@kill.error
async def kill_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Who do you want to be killed?")

#Unban command
@client.command()
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    print(f"The command 'unban' was used in the server: {ctx.guild}")


    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"**User {user.mention} has been unbanned.** :white_check_mark:")
            return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to unban people.")
    if isinstance(error, MissingRequiredArgument):
            await ctx.send("Can you please tell me who to unban?")

#Okboomer command
@client.command()
async def okboomer(ctx):
    await ctx.message.delete()
    await ctx.send("Ok boomer.")
    print(f"The command 'okboomer' was used in the server: {ctx.guild}")

#Notfunny command
@client.command()
async def notfunny(ctx):
    await ctx.send("https://tenor.com/view/bruh-bruh-moment-funny-laugh-not-funny-gif-14520676")
    print(f"The command 'notfunny' was used in the server: {ctx.guild}")

#Lol command
@client.command()
async def lol(ctx):
    await ctx.send("https://media.giphy.com/media/O5NyCibf93upy/giphy.gif")
    print(f"The command 'lol' was used in the server: {ctx.guild}")


#this guy command
@client.command()
async def thisguy(ctx):
    await ctx.send("https://media.giphy.com/media/QWqH7oRfHwVKwb8YDL/giphy.gif")
    print(f"The command 'thisguy' was used in the server: {ctx.guild}")

#No command
@client.command()
async def no(ctx):
    await ctx.send("Yes")
    print(f"The command 'no' was used in the server: {ctx.guild}")

#Yes command
@client.command()
async def yes(ctx):
    await ctx.send("No")
    print(f"The command 'yes' was used in the server: {ctx.guild}")

#Ubuntuhelp command
@client.command()
async def ubuntuhelp(ctx, manual_you_want):
    if manual_you_want == "dualbooting-with-windows" or manual_you_want == "1":
        await ctx.send('''
        1. Get a USB with at *least* 2 GB of storage (4GB recommended).
2. Download Ubuntu, you which ever flavor you want.
3. Burn the `.iso` you just downloaded file on the flash drive with a program called **Balena Etcher**.
4. Time for the hardest part. Making your pc boot off the USB. It depends what company made your computer, but boot into the computer `BIOS` and swich `secure boot` and `fast boot` mode off by highlighting the option and pressing the space bar to turn them off and on. Highlight the `exit and save` button and press enter. It will reboot. Your computer may ask for you to enter a code it displays on-screen and press enter, to verfy that you are a human. When you do that, power off the computer again and boot into the `boot menu`.
5. Highlight your USB's name from the menu, and press the `enter` button.
6. Press "Try Ubuntu without installing" this will not touch any of your hard drives or any information on them.
7. To install, press the "Install" icon on your desktop. Now go to the `install` manual.''')
    if manual_you_want == "install" or manual_you_want == "2":
        await ctx.send('''Great! Now you've booted into your Live USB and you are ready to install ubuntu!
1. Press the "Install" icon on the desktop
2. The Ubiquity install will launch. Just do what it asks you to do.
3. If you are dual booting, select the "Install alongside Windows" option and your done. If you want to wipe Windows, select the "erease disk and install Ubuntu" option.
4. Wait for the installation to finish. It can take up to 15 min.
5. When the installation is complete, remove the USB and reboot your computer. You just dual booted! You can swich between OS when you reboot your machine.''')
        print(f"The command 'ubuntuhelp' was used in the server: {ctx.guild}")

@ubuntuhelp.error
async def ubuntuhelp_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
            await ctx.send('''
            While this bot is made for fun, it can also help with Ubuntu. Availble help guides:

            ```1. install
            2. dualbooting-with-windows```''')


#Running commands through discord
@client.command()
async def run(ctx, *, commandtorun):
    person = ctx.author.id
    if person == int("581965693130506263"):
        commandoutput = subprocess.getoutput(commandtorun)
        if commandoutput == "":
            await ctx.send("Command has been ran. :white_check_mark:")
            return
        await ctx.send(f"```{commandoutput}```")
    if person != int("581965693130506263"):
        await ctx.send("Sorry, but this command is restricted to the owner of this bot and nobody else. Sorry.")
        print(f"The command 'run' was used in the server: {ctx.guild}")


#DM command
@client.command()
async def dm(ctx, member : discord.User, *, message):
    person = ctx.author.id
    if person == int("581965693130506263"):
        await member.send(message)
        await ctx.send("Message sent!")
        return
    await ctx.send("To protect against abuse, this command is only for the creator of this bot.")
    print(f"The command 'DM' was used in the server: {ctx.guild}")

#Mute command
@client.command()
@has_permissions(manage_roles = True)
async def mute(ctx, member: discord.Member):
    guild = ctx.guild
    try:
        mutedrole = discord.utils.get(guild.roles, name='Muted')
        await member.add_roles(mutedrole, reason=None, atomic=True)
        await ctx.send("User muted! :white_check_mark:")
    except:
        await ctx.send("Please make sure that you have a role called `Muted`(notice the capital M) and that you have the `send messages` permission set to denied for every channel for that role.")
    print(f"The command 'mute' was used in the server: {ctx.guild}")


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to mute people.")
    if isinstance(error, MissingRequiredArgument):
            await ctx.send("Can you please tell me who to mute?")

#Unmute command
@client.command()
@has_permissions(manage_roles = True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedrole = discord.utils.get(guild.roles, name='Muted')
    await member.remove_roles(mutedrole, reason=None, atomic=True)
    await ctx.send("User unmuted! :white_check_mark:")
    print(f"The command 'unmute' was used in the server: {ctx.guild}")



@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to unmute people.")
    if isinstance(error, MissingRequiredArgument):
            await ctx.send("Can you please tell me who to unmute?")

#Help command
@client.command()
async def help(ctx):
    person = ctx.author
    await ctx.send(f"Please check your DMs.")
    await person.send('''
A complete list of commands (and more) can be found at https://tribuntu.bss.design/
    ''')

@client.command()
@has_permissions(manage_messages = True)
async def prefix(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=5)

    await ctx.send(f":white_check_mark: Your prefix has been changed to `{prefix}`.")
    print(f"The command 'prefix' was used in the server: {ctx.guild}")


@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to change the bot prefix.")
    if isinstance(error, MissingRequiredArgument):
            await ctx.send("Can you please tell me what to change the server prefix to?")

#Role command
@client.command()
@has_permissions(manage_roles = True)
async def addrole(ctx, member: discord.Member, *, role,):
    guild = ctx.guild
    try:
        therole = discord.utils.get(guild.roles, name=role)
        await member.add_roles(therole, reason=None, atomic=True)
        await ctx.send(f"Role `{therole}` has been added to user {member}. :white_check_mark:")
    except:
        await ctx.send(f":x: I couldn't find the role `{role}`. Please make sure that you typed the **exact** name of the role and try again.")
    print(f"The command 'addrole' was used in the server: {ctx.guild}")


@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to give roles to people.")
    if isinstance(error, MissingRequiredArgument):
            await ctx.send("Can you please tell me what member to add it to, then the role to give to the member?")


#Remove role
@client.command()
@has_permissions(manage_roles = True)
async def removerole(ctx, member: discord.Member, *, role,):
    guild = ctx.guild
    try:
        therole = discord.utils.get(guild.roles, name=role)
        await member.remove_roles(therole, reason=None, atomic=True)
        await ctx.send(f"Role `{therole}` has been removed from user {member}. :white_check_mark:")
    except:
        await ctx.send(f":x: I couldn't find the role `{role}`. Please make sure that you typed the **exact** name of the role and try again.")
    print(f"The command 'removerole' was used in the server: {ctx.guild}")

@removerole.error
async def removerole_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to remove roles from people.")
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Can you please tell me what member to remove it from, then the role to remove from the member?")

# command
@client.command()
async def meme(ctx):
    response = requests.get("https://meme-api.herokuapp.com/gimme")
    response = response.json()
    title = response["title"]
    meme = response["url"]
    embed = discord.Embed(title=title, description=None, color=15105570)
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.set_image(url=f"{meme}")
    await ctx.send(embed=embed)

#Reddit command
@client.command()
async def subreddit(ctx, number_to_get, subreddit_to_get):
    number_to_get = int(number_to_get)
    memes_submissions = reddit.subreddit(f"{subreddit_to_get}").hot()
    post_to_pick = (int(number_to_get))
    post_to_pick_minus_one = post_to_pick - 1
    if number_to_get == 1:
        await ctx.send(f"Getting the current most popular post in the subreddit **{subreddit_to_get}**")
        for i in str(post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
            await ctx.send(submission.url)
    if number_to_get == 2:
        await ctx.send(f"Getting the 2nd current most poplular posts in the subreddit **{subreddit_to_get}**")
        for i in str(post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
            await ctx.send(submission.url)
    if number_to_get == 3:
        await ctx.send(f"Getting the 3rd current most popular post in the subreddit **{subreddit_to_get}**")
        for i in str(post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
            await ctx.send(submission.url)
    if number_to_get >= 4:
        await ctx.send(f"Getting the {number_to_get}th current most poplar post in the subreddit **{subreddit_to_get}**")
        for i in str(post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
            await ctx.send(submission.url)

    print(f"The command 'subreddit' was used in the server: {ctx.guild}")

music_message_authors = {}

play_control_messages = {}

repeat_music_servers = {}


def start_if_true(error):
    for x in client.voice_clients:
        for k, v in repeat_music_servers.items():
            if not x.is_playing():
                if str(x.guild.id) == k:
                    if int(v[-1]) <= 5: 
                        x.play(FFmpegPCMAudio(f"{os.getcwd()}/music/{v[:-1]}.mp3"), after=start_if_true)
                        repeat_music_servers[k] = v[:-1] + str(int(v[-1]) + 1)
                        return
            subprocess.call(f"rm {os.getcwd()}/music/{v[:-1]}.mp3", shell=True)


#Play command
@client.command()
async def play(ctx, *, link):
    global play_control_messages
    try:
        channel = ctx.message.author.voice.channel
    except:
        await ctx.send(":x: Please get in a voice channel, then try again!")
        return


    global music_message_authors
    try:
        if music_message_authors[str(ctx.guild.id)] != ctx.author.id:
            await ctx.send(":x: Please wait until this song is over!")
            return
        global play_control_messages
        del music_message_authors[str(ctx.guild.id)]
        del play_control_messages[str(ctx.guild.id)]
        await ctx.voice_client.disconnect()
    except:
        music_message_authors[str(ctx.guild.id)] = ctx.author.id
    print(music_message_authors)
    subprocess.call("youtube-dl --rm-cache-dir", shell=True)
    the_link_letters = link.find("https://youtu.be/")
    the_link_letters_other = link.find("https://www.youtube.com")
    if the_link_letters_other == 0:
        await ctx.send(":x: You only need the song's name!")
        return
    if the_link_letters != -1:
        await ctx.send(":x: You don't need the link anymore, only the name.")
        return
    video_name_number = random.randint(1, 100000000)
    global voice_name_number
    voice_name_numbers[str(ctx.guild.id)] = str(video_name_number)
    await ctx.channel.trigger_typing()
    play_message_one = await ctx.send("**Please wait up to 10 seconds while the song is being prepared for playback.**")
    subprocess.call(f"youtube-dl --extract-audio --audio-format mp3 -o {os.getcwd()}/tribuntu/music/" + (str(video_name_number)) + ".mp3 " + f'"ytsearch:{link}"', shell=True)
    m = await ctx.send(f"Joining voice channel")
    play_control_messages[str(ctx.guild.id)] = m
    play_control_message = m 
#    duration = subprocess.getoutput("youtube-dl --get-duration " + link)
    global source
    source = FFmpegPCMAudio(f"{os.getcwd()}/music/{video_name_number}.mp3")
    await play_message_one.delete()
    global voice
    voice = await channel.connect()
    player = voice.play(source, after=start_if_true)
    global repeat_music_servers
    await play_control_message.add_reaction("▶")
    await play_control_message.add_reaction("⏸️")
    await play_control_message.add_reaction("❌")
    await play_control_message.edit(content='''Use the reactions to pause/play the music!
*current status*: **Playing**''')
    await play_control_message.add_reaction("🔂")
    global the_channelid
    the_channelid = ctx.channel.id
    global the_message_id
    the_message_id = play_control_message.id
voice_name_numbers = {}


@client.event
async def on_reaction_add(reaction, user):
    global music_message_authors
    global play_control_messages
    global voice_name_numbers
    if user.bot == True:
        return
    try:
        if music_message_authors[str(user.guild.id)] != user.id:
            await reaction.message.channel.send(":x: Please wait until this song is over!")
            return
    except KeyError:
        return
    play_control_message = play_control_messages[str(reaction.message.guild.id)]
    if reaction.emoji == "▶":
        try:
            await play_control_message.remove_reaction("▶", user)
            voice.play(source)
            await play_control_message.edit(content='''Use the reactions to pause/play the music!
*current status:* **Playing**''')
            return
        except:
            pass
    if reaction.emoji == "⏸️":
        try:
            await play_control_message.remove_reaction("⏸️", user)
            voice.pause()
            await play_control_message.edit(content='''Use the reactions to pause/play the music!
*current status:* **Paused**''')
            return
        except:
            pass

    if reaction.emoji == "❌":
        try:
            await play_control_message.clear_reactions()
            voice.stop()
            await voice.disconnect()
            await play_control_message.edit(content='''Use the reactions to pause/play the music!
*current status:* **Canceled/Finished**''')
            del music_message_authors[str(reaction.message.guild.id)]
            del play_control_messages[str(reaction.message.guild.id)]
            return
        except:
            pass
    if reaction.emoji == "🔂":
        await reaction.message.channel.send("**Song will repeat 5 times!**", delete_after=3.0)
        repeat_music_servers[str(reaction.message.guild.id)] = str(voice_name_numbers[str(reaction.message.guild.id)]) + "0"
        await play_control_message.clear_reaction("🔂")


@play.error
async def play_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(":x: **Please give me a song name to play!**")

#Leave a voice channel
@client.command()
async def leave(ctx):
    global music_message_authors
    if music_message_authors[str(ctx.guild.id)] != ctx.author.id:
        await ctx.send(":x: Please wait until this song is over!")
        return


    await ctx.voice_client.disconnect()
    del music_message_authors[str(ctx.guild.id)]
    await ctx.send("**Left the channel.**")

#Restart command
@client.command()
async def restart(ctx):
    person = ctx.author.id
    if person == int("581965693130506263"):
        await ctx.send("Restarting.")
        os.execv(sys.executable, ['python'] + sys.argv)
        return
    await ctx.send("Only the owner of this bot can execute this command.")

#Feedback command
@client.command()
async def feedback(ctx, *, the_feedback):
    person = ctx.author
    with open("userfeedback.txt", "w") as f:
        f.write(f"{person}: {the_feedback}")
        await ctx.send(":white_check_mark: Thank you for your feedback.")


@feedback.error
async def feedback_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Please tell me your feedback.")

#Yeet command
@client.command()
@has_permissions(kick_members = True)
async def yeet(ctx, member : discord.Member):
    await ctx.send(f"**{member} has been yeeted out of the server!**")
    await member.send("**You've been yeeted out the server! Here is your invite back:**")
    channel = ctx.message.channel
    invite_back = await channel.create_invite(max_age=0, max_uses=1)
    await member.send("**Note:** *Invite only has 1 use.*")
    await member.send(invite_back)
    await member.kick(reason="Yeeted out of server.")


@yeet.error
async def yeet_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not has permission to yeet people.")
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Please tell me who to yeet!")


#Poll command
@client.command()
async def poll(ctx, choice_1, choice_2, emoji_1, emoji_2, *, desc):
    embed = discord.Embed(title=desc, description=f"Poll by {ctx.author}", color=0x00ff00)
    choice_1_check = choice_1[0]
    choice_2_check = choice_2[0]
    if choice_1_check == ":" or choice_2_check == ":":
        await ctx.send(":x: Emojis can not be in \"Placeholder\" format. In other words, you can't put `:smile:`, you must put :smile: ")
        return
    embed.add_field(name=choice_1, value=f"Press {emoji_1} to vote for `{choice_1}`", inline=False)
    embed.add_field(name=choice_2, value=f"Press {emoji_2} to vote for `{choice_2}`", inline=False)
    the_message = await ctx.send(embed=embed)
    await the_message.add_reaction(emoji_1)
    await the_message.add_reaction(emoji_2)

@poll.error
async def poll_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("I need choice one, choice two, the emoji for choice one, the emoji for choice two, then the title of the poll. An example would be: ```.poll \"Windows 10\"  \"Windows 7\" \":smile:\" \":frowning:\" \"Which one do you prefer? Windows 7 or 10?\"``` **Inclose multi-word choices in \"\" so I know what is what!**")

@client.command()
@has_permissions(mention_everyone = True)
async def globalpoll(ctx, choice_1, choice_2, emoji_1, emoji_2, *, desc):
    await ctx.send(f"**{ctx.message.guild.default_role} {ctx.author} made a poll:**")
    embed = discord.Embed(title=desc, description=f"Poll by {ctx.author}", color=0x00ff00)
    choice_1_check = choice_1[0]
    choice_2_check = choice_2[0]
    if choice_1_check == ":" or choice_2_check == ":":
        await ctx.send(":x: Emojis can not be in \"Placeholder\" format. In other words, you can't put `:smile:`, you must put :smile: ")
        return
    embed.add_field(name=choice_1, value=f"Press {emoji_1} to vote for {choice_1}", inline=False)
    embed.add_field(name=choice_2, value=f"Press {emoji_2} to vote for {choice_2}", inline=False)
    the_message = await ctx.send(embed=embed)
    await the_message.add_reaction(emoji_1)
    await the_message.add_reaction(emoji_2)

@globalpoll.error
async def globalpoll_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("I need choice one, choice two, the emoji for choice one, the emoji for choice two, then the title of the poll. An example would be: ```.poll \"Windows 10\"  \"Windows 7\" \":smile:\" \":frowning:\" \"Which one do you prefer? Windows 7 or 10?\"``` **Inclose multi-word choices in \"\" so I know what is what!**")
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permission to use a poll with the `@everyone` ping. Use the `.poll` command insted. ")

#Logging on command
@client.command()
@has_permissions(manage_channels = True)
async def logging_on(ctx):
    guild = ctx.message.guild
    await guild.create_text_channel("logs")
    await ctx.send(":white_check_mark: Logging has been turned on! Logs can be found at #tribuntu-logs, to turn off simply delete the channel.")


@logging_on.error
async def logging_on_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Please tell me the category you want me to put the logging channel in.")
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permission to turn on logging.")

#Warn command
@client.command()
@has_permissions(manage_roles = True)
async def warn(ctx, member : discord.Member):
    with open("warned_members.json", "r") as f:
        warned_ones = json.load(f)

    try:
        with open("warned_members.json", "r") as f:
           if warned_ones[str(member)] == 1 or 2 or 3:
               pass
    except:
        with open("warned_members.json", "w") as f:
            warned_ones[str(member)] = 1
            json.dump(warned_ones, f, indent=5)
            await ctx.send(f"{member} has been warned. You have been warned **1** time so far, and have **2** warns left until a mute.")
            return
    if warned_ones[str(member)] == 1:
        warned_ones[str(member)] = 2
        with open("warned_members.json", "w") as f:
            json.dump(warned_ones, f, indent=5)
            await ctx.send(f"{member} has been warned. You have been warned **2** times so far, and have **1** warn left until a mute.")
            return
    if warned_ones[str(member)] == 2:
        try:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.add_roles(muted_role, reason=None, atomic=True)
            warned_ones.pop(str(member))
            with open("warned_members.json", "w") as f:
                json.dump(warned_ones, f, indent=5)
                await ctx.send(f"{member} has been muted for getting 3 warns.")
        except:
            await ctx.send(":x: You have not set up a `Muted` role. Once you have set it up, then try again.")


    the_guild = ctx.guild
    the_channel = discord.utils.get(the_guild.text_channels, name="logs")
    the_author = ctx.author
    embed = discord.Embed(title="Member Warned", description=f"{the_author} has warned {member}. {member} has been warned {warned_ones[str(member)]} time(s).", color=3447003)
    await the_channel.send(embed=embed)


@warn.error
async def warn_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Who would you like to warn?")
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permission to warn people.")

#Get user profile picture
@client.command()
async def pfp(ctx, member : discord.User):
    profile_picture = member.avatar_url
    profile_picture = str(profile_picture)
    await ctx.send(profile_picture)

#Level command
@client.command()
async def level(ctx, member : discord.User):
    message_author = member.id
    with open("levelups.json", "r") as f:
        file_contents = json.load(f)
        the_user_messages = file_contents[str(member.id)]

    if file_contents[str(message_author)] > 0 and file_contents[str(message_author)] < 50:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **0**.")

    if file_contents[str(message_author)] >= 50 and file_contents[str(message_author)] < 100:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **1**.")

    if file_contents[str(message_author)] >= 100 and file_contents[str(message_author)] < 150:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **2**.")

    if file_contents[str(message_author)] >= 150 and file_contents[str(message_author)] < 200:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **3**.")

    if file_contents[str(message_author)] >= 200 and file_contents[str(message_author)] < 250:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **4**.")

    if file_contents[str(message_author)] >= 250 and file_contents[str(message_author)] < 300:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **5**.")

    if file_contents[str(message_author)] >= 300 and file_contents[str(message_author)] < 350:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **6**.")

    if file_contents[str(message_author)] >= 350 and file_contents[str(message_author)] < 400:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **7**.")

    if file_contents[str(message_author)] >= 400 and file_contents[str(message_author)] < 450:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **8**.")

    if file_contents[str(message_author)] >= 450 and file_contents[str(message_author)] < 500:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **9**.")

    if file_contents[str(message_author)] >= 500:
        await ctx.send(f"{member} has sent **{the_user_messages}** messages and is on level **10**")

@level.error
async def level_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Please tell me the person so I can see what level they are on.")

#Disable ranking system
@client.command()
@has_permissions(administrator = True)
async def ranking_off(ctx):
    with open("levelups_disabled.json", "r") as f:
        contents = json.load(f)
    with open("levelups_disabled.json", "w") as f:
        contents[str(ctx.guild.id)] = "Disabled"
        json.dump(contents, f)
    await ctx.send(":white_check_mark: Ranking messages have been disabled for this server. To re-enable it, use the `.ranking_on` command.")

@ranking_off.error
async def ranking_off_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permissions to turn off ranking")

#Enable ranking system
@client.command()
@has_permissions(administrator = True)
async def ranking_on(ctx):
    with open("levelups_disabled.json", "r") as f:
        contents = json.load(f)
    with open("levelups_disabled.json", "w") as f:
        contents.pop(str(ctx.guild.id))
        json.dump(contents, f)
    await ctx.send(":white_check_mark: Ranking messages have been enabled for this server. To disable it, use the `.ranking_off` command.")

@ranking_on.error
async def ranking_on_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permissions to turn on ranking")

#Join command
@client.command()
async def join(ctx):
    await ctx.send("No need to use this command. Use the `.play` command insted please.")

#Custom command
#@client.command()
#async def addcommand(ctx, command_to_add, *, response):
#   with open("custom_commands.json", "w") as f:
#       file_contents = json.load(f)
#       file_contents[str(f"{ctx.guild.id}_{command_to_add}")] = file_contents[str(f"{response}")]
#       json.dump(file_contents, f)

#Profile command
@client.command()
async def profile(ctx, The_user_to_get_profile_from : discord.Member):
#    the_user = ctx.guild.get_member(The_user_to_get_profile_from.id)
#    user_list = []
#    for users in ctx.guild.fetch_members():
#        user_list.append(user)
#
#    if The_user_to_get_profile_from in user_list:
#        The_user_to_get_profile_from = The_user_to_get_profile_from : discord.Member
#
#
    userid = ctx.author.id
    f = open("warned_members.json", "r")
    warned_ones_file = json.load(f)
#   for The_user_to_get_profile_from.roles in The_user_to_get_profile_from.roles:
#       The_user_to_get_profile_from_roles = The_user_to_get_profile_from.roles.split(",")
#   l = ", "
#   l = l.join(f"{The_user_to_get_profile_from.roles}")
    number = random.randint(1, 100)
    embed = discord.Embed(title="Profile Description", description=f"Requested by {ctx.author}", color=3447003)
    embed.add_field(name="Account Name:", value=f"{The_user_to_get_profile_from.name}")
    embed.set_image(url=f"{The_user_to_get_profile_from.avatar_url}")
#   embed.add_field(name=f"Roles:", value=f"{l}", inline=False)
    embed.add_field(name="Account Creation Date:", value=f"{The_user_to_get_profile_from.created_at}")
    embed.add_field(name="Bot:", value=f"{The_user_to_get_profile_from.bot}")
    embed.add_field(name="Animated Profile Picture:", value=f"{The_user_to_get_profile_from.is_avatar_animated()}")
    embed.add_field(name="Discriminator:", value=f"{The_user_to_get_profile_from.discriminator}")
    try:
        embed.add_field(name="Server Nickname:", value=f"{The_user_to_get_profile_from.nick}")
    except:
        embed.set_footer(text="Information about this user may be limited because they are not in this server.")
    try:
        embed.add_field(name="Warns:", value=f"{warned_ones_file[str(The_user_to_get_profile_from)]}")
    except:
        embed.add_field(name="Warns:", value="0")
    try:
        embed.add_field(name="Status:", value=f"{The_user_to_get_profile_from.status}")
    except:
        pass
    try:
        embed.add_field(name="Is On Mobile Device:", value=f"{The_user_to_get_profile_from.is_on_mobile()}")
    except:
        pass
    try:
        embed.add_field(name="Activity:", value=f"{The_user_to_get_profile_from.activity.name}")
    except:
        embed.add_field(name="Activity:", value="None")
    try:
        permission_list = []
        for p, t in The_user_to_get_profile_from.guild_permissions:
            if t == False:
                continue
            permission_list.append(p)
        embed.add_field(name="Permissions", value=str(permission_list))
    except:
        pass
    embed.add_field(name="User ID:", value=f"{The_user_to_get_profile_from.id}")
    with open("levelups.json", "r") as f:
        file = json.load(f)
        try:
            embed.add_field(name="Messages Sent:", value=f"{file[str(The_user_to_get_profile_from.id)]}")
        except:
            pass
    await ctx.send(embed=embed)
    f.close()
    permission_list.clear()


@profile.error
async def profile_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        The_user_to_get_profile_from = ctx.author
        userid = ctx.author.id
        f = open("warned_members.json", "r")
        warned_ones_file = json.load(f)
    #   for The_user_to_get_profile_from.roles in The_user_to_get_profile_from.roles:
    #       The_user_to_get_profile_from_roles = The_user_to_get_profile_from.roles.split(",")
    #   l = ", "
    #   l = l.join(f"{The_user_to_get_profile_from.roles}")
        number = random.randint(1, 100)
        embed = discord.Embed(title="Profile Description", description=f"Requested by {ctx.author}", color=3447003)
        embed.add_field(name="Account Name:", value=f"{The_user_to_get_profile_from.name}")
        embed.set_image(url=f"{The_user_to_get_profile_from.avatar_url}")
    #   embed.add_field(name=f"Roles:", value=f"{l}", inline=False)
        embed.add_field(name="Account Creation Date:", value=f"{The_user_to_get_profile_from.created_at}")
        embed.add_field(name="Bot:", value=f"{The_user_to_get_profile_from.bot}")
        embed.add_field(name="Animated Profile Picture:", value=f"{The_user_to_get_profile_from.is_avatar_animated()}")
        embed.add_field(name="Discriminator:", value=f"{The_user_to_get_profile_from.discriminator}")
        try:
            embed.add_field(name="Server Nickname:", value=f"{The_user_to_get_profile_from.nick}")
        except:
            embed.set_footer(text="Information about this user may be limited because they are not in this server.")
        try:
            embed.add_field(name="Warns:", value=f"{warned_ones_file[str(The_user_to_get_profile_from)]}")
        except:
            embed.add_field(name="Warns:", value="0")
        try:
            embed.add_field(name="Status:", value=f"{The_user_to_get_profile_from.status}")
        except:
            pass
        try:
            embed.add_field(name="Is On Mobile Device:", value=f"{The_user_to_get_profile_from.is_on_mobile()}")
        except:
            pass
        try:
            embed.add_field(name="Activity:", value=f"{The_user_to_get_profile_from.activity.name}")
        except:
            embed.add_field(name="Activity:", value="None")
        embed.add_field(name="User ID:", value=f"{The_user_to_get_profile_from.id}")
        try:
            permission_list = []
            for p, t in ctx.author.guild_permissions:
                if t == False:
                    continue
                permission_list.append(p)
            embed.add_field(name="Permissions", value=str(permission_list))
        except:
            pass
        with open("levelups.json", "r") as f:
            file = json.load(f)
            embed.add_field(name="Messages Sent:", value=f"{file[str(The_user_to_get_profile_from.id)]}")
        await ctx.send(embed=embed)
        f.close()
        permission_list.clear()

    if isinstance(error, BadArgument):
        The_user_to_get_profile_from = f"{error}".split('"') #Split it into the ID/Username
        The_user_to_get_profile_from = The_user_to_get_profile_from[1]
        try:
            int_object = int(The_user_to_get_profile_from)
            The_user_to_get_profile_from = client.get_user(int_object)
        except:
                if str(The_user_to_get_profile_from[0]) == "@":
                    The_user_to_get_profile_from = f"{The_user_to_get_profile_from[1:]}"
#                for x in client.guilds:
#                    try:
#                        The_user_to_get_profile_from = x.get_user_by_name(f"{The_user_to_get_profile_from}")
#                    except:
#                        continue
#
                if ctx.author.id == int("581965693130506263"):
                    if f"{The_user_to_get_profile_from}".find("#") == -1:
                        for u in client.get_all_members():
                            if f"{The_user_to_get_profile_from}" == f"{u}"[:-5]:
                                The_user_to_get_profile_from = u

                    if f"{The_user_to_get_profile_from}".find("#") != -1:
                        for u in client.get_all_members():
                            if f"{The_user_to_get_profile_from}" == f"{u}":
                                The_user_to_get_profile_from = u


                if ctx.author.id != int("581965693130506263"):
                    for u in client.get_all_members():
                        if f"{u}" == f"{The_user_to_get_profile_from}":
                            The_user_to_get_profile_from = u

        userid = ctx.author.id
        f = open("warned_members.json", "r")
        warned_ones_file = json.load(f)
    #   for The_user_to_get_profile_from.roles in The_user_to_get_profile_from.roles:
    #       The_user_to_get_profile_from_roles = The_user_to_get_profile_from.roles.split(",")
    #   l = ", "
    #   l = l.join(f"{The_user_to_get_profile_from.roles}")
        number = random.randint(1, 100)
        embed = discord.Embed(title="Profile Description", description=f"Requested by {ctx.author}", color=3447003)
        embed.set_footer(text="Information about this user may be limited because they are not in this server.")
        embed.add_field(name="Account Name:", value=f"{The_user_to_get_profile_from.name}")
        embed.set_image(url=f"{The_user_to_get_profile_from.avatar_url}")
    #   embed.add_field(name=f"Roles:", value=f"{l}", inline=False)
        embed.add_field(name="Account Creation Date:", value=f"{The_user_to_get_profile_from.created_at}")
        embed.add_field(name="Bot:", value=f"{The_user_to_get_profile_from.bot}")
        embed.add_field(name="Animated Profile Picture:", value=f"{The_user_to_get_profile_from.is_avatar_animated()}")
        embed.add_field(name="Discriminator:", value=f"{The_user_to_get_profile_from.discriminator}")
        try:
            embed.add_field(name="Server Nickname:", value=f"{The_user_to_get_profile_from.nick}")
        except:
            embed.set_footer(text="Information about this user is limited because they are not in this server.")
        try:
            embed.add_field(name="Warns:", value=f"{warned_ones_file[str(The_user_to_get_profile_from)]}")
        except:
            pass
        try:
            embed.add_field(name="Status:", value=f"{The_user_to_get_profile_from.status}")
        except:
            pass
        try:
            embed.add_field(name="Is On Mobile Device:", value=f"{The_user_to_get_profile_from.is_on_mobile()}")
        except:
            pass
        try:
            embed.add_field(name="Activity:", value=f"{The_user_to_get_profile_from.activity.name}")
        except:
            embed.add_field(name="Activity:", value="None")
        embed.add_field(name="User ID:", value=f"{The_user_to_get_profile_from.id}")
        with open("levelups.json", "r") as f:
            file = json.load(f)
            try:
                embed.add_field(name="Messages Sent:", value=f"{file[str(The_user_to_get_profile_from.id)]}")
            except KeyError:
                embed.add_field(name="Messages Sent:", value="0")

        await ctx.send(embed=embed)
        f.close()


#Info command for the bot
@client.command()
async def info(ctx):

    all_members_embed_list = []

    for x in client.get_all_members():
        all_members_embed_list.append(x)

        client_embed_guilds = []

        for t in client.guilds:
            client_embed_guilds.append(t)

    embed = discord.Embed(title="Bot Info", description="General info about Tribuntu", color=11027200)
    embed.set_thumbnail(url="https://149366088.v2.pressablecdn.com/wp-content/uploads/2019/09/ermine-logo-300x300.png")
    embed.add_field(name="Bot Author and Maintainer:", value="TricolorHen061#1443", inline=True)
    embed.add_field(name="Number of members being watched:", value=f"{len(all_members_embed_list)}", inline=True)
    embed.add_field(name="Number of servers Tribuntu is in:", value=f"{len(client_embed_guilds)}", inline=True)
    embed.add_field(name="Website:", value="https://tribuntu.bss.design/", inline=True)
    await ctx.send(embed=embed)



#@client.command()
#async def loggingoff(ctx):
#    with open("disabled_logging", "r") as f:
#        file_contents = json.load(f)
#        with open ("disabled_logging", "w") as g:
#            file.contents.pop(str(f"{ctx.author.id}"))
#            file_contents.dump(file_contents, g)
#            await ctx.send(":white_check_mark: You will be logged.")
#
#
#@client.command()
#async def loggingon(ctx):
#    with open("disabled_logging", "r") as f:
#        file_contents = json.load(f)
#        with open ("disabled_logging", "w") as g:
#            file_contents[str(f"{ctx.author.id}")] = "Disabled"
#            file_contents.dump(file_contents, g)
#            await ctx.send(":white_check_mark: You will not be logged anymore.")

#Command to start memes in minute-memes channel
@client.command()
@has_permissions(manage_messages = True)
async def start_memes(ctx):
    the_channel = discord.utils.get(ctx.guild.text_channels, name="minute-memes")

    if not the_channel:
        await ctx.send(":x: You need to make a channel called 'minute-memes' first!")
        return

    with open("meme_channels.json", "r") as r:
        content = json.load(r)
        with open("meme_channels.json", "w") as w:
            content.append(f"{ctx.guild.id}")
            json.dump(content, w)
    await ctx.send(":white_check_mark: You will now get memes every 5 minutes in #minute-memes.")

@start_memes.error
async def start_memes_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(":x: You do not have permission to start memes")

#Command to stop memes in minute-memes channel
@client.command()
@has_permissions(manage_channels = True)
async def stop_memes(ctx):
    with open("meme_channels.json", "r") as r:
        the_content = json.load(r)

        with open("meme_channels.json", "w") as w:
            the_content.remove(str(f"{ctx.guild.id}"))
            json.dump(the_content, w)
    await ctx.send(":white_check_mark: Memes will no longer be sent in #minute-memes.")

@stop_memes.error
async def stop_memes_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(":x: You do not have permissions to stop memes.")


@client.command()
async def changepoints(ctx, user : discord.Member, amount_of_points_to_change):
    if ctx.author.id == int("581965693130506263"):
        with open("levelups.json", "r") as k:
            file_content = json.load(k)
            with open("levelups.json", "w") as b:
                file_content[str(f"{user.id}")] = int(amount_of_points_to_change)
                json.dump(file_content, b, indent=5)
        await ctx.send(f":white_check_mark: {user.name}'s points have been modified.")

    elif ctx.author.id != int("581965693130506263"):
        await ctx.send("Only the owner of this bot can use this command.")

#Change status command
@client.command()
async def changestatus(ctx, the_status):
    if ctx.author.id == int("581965693130506263"):
        if the_status == "online":
            await client.change_presence(status=discord.Status.online)
            await ctx.send(":white_check_mark: The bot's status has been changed.")

        if the_status == "idle":
            await client.change_presence(status=discord.Status.idle)
            await ctx.send(":white_check_mark: The bot's status has been changed.")

        if the_status == "dnd":
            await client.change_presence(status=discord.Status.dnd)
            await ctx.send(":white_check_mark: The bot's status has been changed.")

        if the_status == "offline":
            await client.change_presence(status=discord.Status.offline)
            await ctx.send(":white_check_mark: The bot's status has been changed.")

    elif ctx.author.id != int("581965693130506263"):
        await ctx.send("Only the owner of this bot can use this command."

@client.command()
async def rps(ctx):
    choices_to_choose_from = ["rock", "paper", "scissors"]
    selection = random.choice(choices_to_choose_from)
    if selection == "rock":
        await ctx.send("rock")
    if selection == "paper":
        await ctx.send("Paper")
    if selection == "scissors":
        await ctx.send("Scissors")

#Coronavirus/COVID-19 command
@client.command()
async def coronavirusinfo(ctx):
    coronavirus_infomation = requests.get("https://corona.lmao.ninja/v2/all")
    coronavirus_infomation = coronavirus_infomation.json()
    embed = discord.Embed(title="Coronavirus Infomation", description=None)
    embed.set_thumbnail(url="https://www.cdc.gov/media/dpk/diseases-and-conditions/coronavirus/images/outbreak-coronavirus-world-1024x506px.jpg")
    embed.add_field(name="Cases of the Coronavirus:", value=coronavirus_infomation["cases"])
    embed.add_field(name="Deaths from the Coronavirus:", value=coronavirus_infomation["deaths"])
    embed.add_field(name="People Recovered:", value=coronavirus_infomation["recovered"])
    await ctx.send(embed=embed)


#Runs the bot
client.run("") # Put your bot token here
