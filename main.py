from mysql.connector import (connection, MySQLConnection, Error)

cnx = connection.MySQLConnection(user='root', password='pass',
                                 host='127.0.0.1',
                                 database='bot')

# Connection test
cursor = cnx.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print('Total Row(s):', cursor.rowcount)
cursor.close()
# End Connection test

import discord
from discord.ext import commands
from asyncio import *
from time import *
import json
import random


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
                'pedar',
                'response', 'responses']


@client.event
async def on_message(infox):
    cursor = cnx.cursor()
    sql = "SELECT * FROM responses WHERE response_to = '{0}'".format(infox.content)
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    if infox.content[0:1] == ']':
        command = infox.content[1:].split()[0]
        if command not in all_commands:
            await infox.channel.send(">>> " + infox.author.mention + " In command vojud nadarad!")

        else:
            await client.process_commands(infox)

    else:
        if row:
            cursor = cnx.cursor()
            sql = "SELECT * FROM response WHERE response_id = '{0}'".format(row[0])
            cursor.execute(sql)
            responses = cursor.fetchall()
            cursor.close()
            random_response = random.choice(responses)
            response_text = random_response[2]
            await infox.channel.send(
                "{0}".format(response_text))

        cursor = cnx.cursor()
        sql = "SELECT * FROM users WHERE username = {0} AND guild = {1}".format(infox.author.id, infox.guild.id)
        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        if row:
            new_score = int(row[2]) + 5
            cursor = cnx.cursor()
            sql = "UPDATE users SET score = {0} WHERE idusers = {1}".format(new_score, row[0])
            cursor.execute(sql)
            cnx.commit()
            cursor.close()
            if new_score % 100 == 0:
                rank = new_score // 100
                await infox.channel.send(
                    ">>> " + infox.author.mention + " shoma be levele " + str(rank) + " residid, mobarake :)) ")

        else:
            cursor = cnx.cursor()
            sql = "INSERT INTO users (username, score, guild) VALUES ({0}, {1}, {2}) ".format(infox.author.id, 0, infox.guild.id)
            cursor.execute(sql)
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
    help_embed.set_author(name="MahyarNV", url='http://mbehzadi.ir')
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
            await infox.send(">>> " + infox.author.mention + ' Status e morede nazar vojud nadarad be mola!')

    else:
        await infox.send(">>> " + infox.author.mention + " dastresi nadari be mola!")


@client.command(aliases=['activity', 'act', 'active'])
async def command_activity(infox, act_type='', *, act_text='...'):
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
                await infox.send(">>> " + infox.author.mention + ' activitie e morede nazar vojud nadarad be mola!')

        else:
            await infox.send(">>> " + infox.author.mention + " activitie bayad matn dashte bashe be mola!")

    else:
        await infox.send(">>> " + infox.author.mention + " dastresi nadari be mola!")


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
    sql = "SELECT * FROM users WHERE username = {0} AND guild = {1}".format(infox.author.id, infox.guild.id)
    cursor.execute(sql)
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
            role = discord.utils.get(infox.guild.roles, name="Muted")
            await member.add_roles(role)
            await infox.send(">>> " + infox.author.mention + " user e morede nazar mute shod!")

        else:
            await infox.send(">>> " + infox.author.mention + " bayad memberi ra mention konid!")

    else:
        await infox.send(">>> " + infox.author.mention + " dastresi nadari be mola!")


@client.command(aliases=['unmute', 'Unmute', 'unMute', 'UnMute'])
async def command_unmute(infox, member: discord.Member = ''):
    if infox.message.author.guild_permissions.administrator:
        if member != '':
            role = discord.utils.get(infox.guild.roles, name="Muted")
            await member.remove_roles(role)
            await infox.send(">>> " + infox.author.mention + " user e morede nazar unmute shod!")

        else:
            await infox.send(">>> " + infox.author.mention + " bayad memberi ra mention konid!")

    else:
        await infox.send(">>> " + infox.author.mention + " dastresi nadari be mola!")


@client.command(aliases=['response'])
async def command_response(infox, action='', response_to='', responses=''):
    if infox.message.author.guild_permissions.administrator:
        if response_to != '' and responses !='' and action !='':
            if action == 'add':
                cursor = cnx.cursor()
                sql = "SELECT * FROM responses WHERE response_to = '{0}'".format(response_to)
                cursor.execute(sql)
                row = cursor.fetchone()
                cursor.close()
                if  not row:
                    response_to = str(response_to.strip('''"'''))
                    responses = responses.strip('''"''').split('''--''')
                    if response_to not in responses:
                        while True:
                            gen_id = random.randint(100000, 999999)
                            cursor = cnx.cursor()
                            sql = "SELECT * FROM responses WHERE gen_id = {0}".format(gen_id)
                            cursor.execute(sql)
                            row = cursor.fetchone()
                            cursor.close()
                            if not row:
                                break

                        cursor = cnx.cursor()
                        sql = "INSERT INTO responses (gen_id, guild, response_to) VALUES ({0}, {1}, '{2}')".format(gen_id, infox.guild.id, response_to)
                        cursor.execute(sql)
                        res_id = cursor.lastrowid
                        cnx.commit()
                        cursor.close()
                        for response in responses:
                            cursor = cnx.cursor()
                            sql = "INSERT INTO response (response_id, text) VALUES ({0}, '{1}')".format(res_id, response)
                            cursor.execute(sql)
                            cnx.commit()
                            cursor.close()

                        await infox.send(">>> " + infox.author.mention + " response add shod!")

                    else:
                        await infox.send(">>> " + infox.author.mention + " text ba responsesh nemitune yeki bashe!")

                else:
                    await infox.send(">>> " + infox.author.mention + " ino ghablan add dade budi, mituni deletesh koni!")

            elif action == 'edit':
                pass

        elif action == 'delete':
            cursor = cnx.cursor()
            sql = "SELECT * FROM responses WHERE gen_id = {0}".format(int(response_to))
            cursor.execute(sql)
            row = cursor.fetchone()
            cursor.close()
            if row:
                cursor = cnx.cursor()
                sql = "SELECT * FROM response WHERE response_id = {0}".format(row[0])
                cursor.execute(sql)
                responses = cursor.fetchall()
                cursor.close()
                for response in responses:
                    cursor = cnx.cursor()
                    sql = "DELETE FROM response WHERE id = {0}".format(response[0])
                    cursor.execute(sql)
                    cnx.commit()
                    cursor.close()

                cursor = cnx.cursor()
                sql = "DELETE FROM responses WHERE gen_id = {0}".format(int(response_to))
                cursor.execute(sql)
                cnx.commit()
                cursor.close()
                await infox.send(">>> " + infox.author.mention + " response delete shod!")

            else:
                await infox.send(">>> " + infox.author.mention + " hamchin responsi sabt nashode bud!")

        else:
            await infox.send(">>> " + infox.author.mention + " meghdar nadadi be mola!")

    else:
        await infox.send(">>> " + infox.author.mention + " dastresi nadari be mola!")


@client.command(aliases=['responses'])
async def command_responses(infox):
    if infox.message.author.guild_permissions.administrator:
        cursor = cnx.cursor()
        sql = "SELECT * FROM responses WHERE guild = '{0}'".format(infox.guild.id)
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            description = "{0} responses: \n".format(len(rows))
            for row in rows:
                cursor = cnx.cursor()
                sql = "SELECT * FROM response WHERE response_id = '{0}'".format(row[0])
                cursor.execute(sql)
                responses = cursor.fetchall()
                cursor.close()
                responses_text = ''
                for response in responses:
                    responses_text += '"{0}" '.format(response[2])
                description += "id: ||{0}||, respond to: {1}, responses: {2} \n\n".format(row[1], row[3], responses_text)
            responses_embed = discord.Embed(
                colour=0x0A75AD,
                title="Responses",
                description=description
                )
            responses_embed.set_footer(text='shoma mitavanaid id ra copy konid baraye edit va delete kardane response')

        else:
            responses_embed = discord.Embed(
                colour=0x0A75AD,
                title="Responses",
                description="ta be haal responsi add nakardid!"
                )
            responses_embed.set_footer(text="shoma mitavanaid response add konid ba ']response add' (etela'te kame tar ba ]help)")

        responses_embed.set_author(name="MahyarNV", url='http://mbehzadi.ir')
        await infox.send(embed=responses_embed)

    else:
        await infox.send(">>> " + infox.author.mention + " dastresi nadari be mola!")


client.run(CONFIG.TOKEN)
