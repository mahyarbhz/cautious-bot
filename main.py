import discord
from discord.ext import commands
from asyncio import *
from time import *


class CONFIG:
    TOKEN = ''
    PREFIX = ']'


client = commands.Bot(command_prefix=CONFIG.PREFIX)
client.remove_command('help')


@client.event
async def on_ready():
    print('Bot Onlined')


all_commands = ['help', 'helps', 'helper', 'helping',
                'GG', 'Gg', 'gg', 'gG',
                'status', 'setstatus', 'setst', 'set_status',
                'activity', 'act', 'active',
                'clear', 'cl']


@client.event
async def on_message(infox):
    if infox.content[0:1] == ']':
        command = infox.content[1:].split()[0]
        if command not in all_commands:
            await infox.channel.send(">>> " + infox.author.mention + " In command vojud nadarad!")
        else:
            await client.process_commands(infox)
    else:
        pass


@client.command(aliases=['help', 'helps', 'helper', 'helping'])
async def command_help(infox):
    help_embed = discord.Embed(
        colour=0x0A75AD,
        title="Help ❓",
        description="Dastoorate Admin ha:\n```]status [status]```\n```]activity [activity(playing, watching, "
                    "listening)]```\n```]clear [meghdar]``` "
    )
    help_embed.set_footer(text='Hope you used this helps')
    help_embed.set_author(name="MahyarNV", url='http://test.mbehzadi.ir')
    await infox.send(embed=help_embed)


@client.command(aliases=['GG', 'Gg', 'gg', 'gG'])
async def command_gg(infox, *, pos='person'):
    await infox.send(">>> " + infox.author.mention + ' you are a GG ' + pos + ' ;)')


@client.command(aliases=['status', 'setstatus', 'setst', 'set_status'])
async def command_status(infox, status_type):
    if infox.message.author.guild_permissions.administrator:

        if status_type == 'idle':
            await client.change_presence(status=discord.Status.idle)
            print('taghire status be idle')

        elif status_type == 'dnd':
            await client.change_presence(status=discord.Status.dnd)

        elif status_type == 'online':
            await client.change_presence(status=discord.Status.online)

        else:
            await infox.send(">>> " + infox.author.mention + ' Status e morede nazar vojud nadarad!')

    else:
        await infox.send(">>> " + infox.author.mention + " you don't have permission to do that❗❌")


@client.command(aliases=['activity', 'act', 'active'])
async def command_activity(infox, act_type='', *, act_text='...'):
    if infox.message.author.guild_permissions.administrator:

        if act_type == 'playing':
            await client.change_presence(activity=discord.Game(name=act_text))

        elif act_type == 'watching':
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=act_text))

        elif act_type == 'listening':
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=act_text))

        else:
            await infox.send(">>> " + infox.author.mention + ' Status e morede nazar vojud nadarad!')

    else:
        await infox.send(">>> " + infox.author.mention + " you don't have permission to do that❗❌")


@client.command(aliases=['clear', 'cl'])
async def command_clear(infox, clear_count=0):
    if clear_count == 0:
        await infox.send("0 message nemitavanad pak shavad❌")
    else:
        await infox.channel.purge(limit=int(clear_count) + 1)
        await infox.send(">>> " + str(clear_count) + " message pak shod✔")
        # sleep(2)
        # await infox.channel.purge(limit=1)

# End Incomplete branch
client.run(CONFIG.TOKEN)
