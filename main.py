from mysql.connector import (connection, MySQLConnection, Error)

cnx = connection.MySQLConnection(user='root', password='pass',
                                 host='127.0.0.1',
                                 database='bot')

# Connection test
cursor = cnx.cursor()
cursor.execute(("SELECT * FROM users"))
rows = cursor.fetchall()
print('Total Row(s):', cursor.rowcount)
cursor.close()
# End Connection test

import discord
from discord.ext import commands
from discord.utils import get
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
                'clear', 'cl',
                'rank', 'score', 'level',
                'mute', 'Mute',
                'unmute', 'Unmute', 'unMute', 'UnMute'
                'pedar']


@client.event
async def on_message(infox):
    if infox.content[0:1] == ']':
        command = infox.content[1:].split()[0]
        if command not in all_commands:
            await infox.channel.send(">>> " + infox.author.mention + " In command vojud nadarad!")

        else:
            await client.process_commands(infox)

    else:
        cursor = cnx.cursor()
        cursor.execute(("SELECT * FROM users WHERE username LIKE " + str(infox.author.id) + " AND guild LIKE " + str(infox.guild.id)))
        row = cursor.fetchone()
        cursor.close()
        if row:
            new_score = int(row[2]) + 5
            cursor = cnx.cursor()
            cursor.execute("UPDATE users SET score=%d WHERE idusers='%d'" % (new_score, row[0]))
            cnx.commit()
            cursor.close()
            if new_score % 100 == 0:
                rank = new_score // 100
                await infox.channel.send(
                    ">>> " + infox.author.mention + " shoma be levele " + str(rank) + " residid, mobarake :)) ")

        else:
            cursor = cnx.cursor()
            cursor.execute("INSERT INTO users (username, score, guild) VALUES (%d, %d, %d) " % (infox.author.id, 0, infox.guild.id))
            cnx.commit()
            cursor.close()


@client.command(aliases=['help', 'helps', 'helper', 'helping'])
async def command_help(infox):
    help_embed = discord.Embed(
        colour=0x0A75AD,
        title="Help ❓",
        description="Dastoorate admin ha:" \
                    "```]status [status]```" \
                    "```]activity [activity] [matn]```" \
                    "```]clear [meghdar]```" \
                    "```]mute [mention]```" \
                    "```]unmute [mention]```" \
                    "\n" \
                    "Dastoorate public:" \
                    "```]rank```"
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
    print(infox)
    if infox.message.author.guild_permissions.administrator:
        if act_text != '...':
            if act_type == 'playing':
                await client.change_presence(activity=discord.Game(name=act_text))

            elif act_type == 'watching':
                await client.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.watching, name=act_text))

            elif act_type == 'listening':
                await client.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.listening, name=act_text))

            else:
                await infox.send(">>> " + infox.author.mention + ' Status e morede nazar vojud nadarad!')

        else:
            await infox.send(">>> " + infox.author.mention + " status bayad matn dashte bashad")

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


@client.command(aliases=['rank', 'score', 'level'])
async def command_rank(infox):
    cursor = cnx.cursor()
    cursor.execute(("SELECT * FROM users WHERE username LIKE " + str(infox.author.id) + " AND guild LIKE " + str(infox.guild.id)))
    row = cursor.fetchone()
    cursor.close()
    if row:
        score = int(row[2])
        await infox.send(">>> " + infox.author.mention + " ranke shoma " + str(score // 100) + " ast!")

    else:
        await infox.send(">>> " + infox.author.mention + " shoma leveli nadarid!")


@client.command(aliases=['mute', 'Mute'])
async def command_mute(infox, member: discord.Member = ''):
    if infox.message.author.guild_permissions.administrator:
        if member != '':
            role = get(infox.guild.roles, name="Muted")
            await member.add_roles(role)
            await infox.send(">>> " + infox.author.mention + " user e morede nazar mute shod!")

        else:
            await infox.send(">>> " + infox.author.mention + " bayad memberi ra mention konid!")

    else:
        await infox.send(">>> " + infox.author.mention + " dastresie lazem baraye mute kardan nadarid!")


@client.command(aliases=['unmute', 'Unmute', 'unMute', 'UnMute'])
async def command_unmute(infox, member: discord.Member = ''):
    if infox.message.author.guild_permissions.administrator:
        if member != '':
            role = get(infox.guild.roles, name="Muted")
            await member.remove_roles(role)
            await infox.send(">>> " + infox.author.mention + " user e morede nazar unmute shod!")

        else:
            await infox.send(">>> " + infox.author.mention + " bayad memberi ra mention konid!")

    else:
        await infox.send(">>> " + infox.author.mention + " dastresie lazem baraye mute kardan nadarid!")


client.run(CONFIG.TOKEN)
