from mysql.connector import (connection, MySQLConnection, Error)

cnx = connection.MySQLConnection(user='root', password='',
                                 host='127.0.0.1',
                                 database='bot')

# Connection test
cursor = cnx.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print('Total Row(s):', cursor.rowcount)
cursor.close()
# End Connection test

def truncate(table):
    cursor = cnx.cursor()
    cursor.execute("truncate {0}".format(table))
    cnx.commit()
    cursor.close()

# truncate('users')

import discord
from discord.ext import commands
from asyncio import *
from time import *
import json
import random


class CONFIG:
    TOKEN = ''
    BOT_ID = ''
    PREFIX = '>'


client = commands.Bot(command_prefix=CONFIG.PREFIX)
client.remove_command('help')


@client.event
async def on_ready():
    print('Bot Onlined')


@client.event
async def on_command_error(infox, error):
    if isinstance(error, commands.CommandNotFound):
        await infox.channel.send(">>> {0} in command vojud nadarad!".format(infox.author.mention))

    if isinstance(error, commands.MissingPermissions):
        await infox.send(">>> {0} shoma dastresie in kar ra nadarid❌".format(infox.author.mention))


@client.event
async def on_message(infox):
    cursor = cnx.cursor()
    sql = "SELECT * FROM responses WHERE response_to = '{0}' AND guild = {1}".format(infox.content, infox.guild.id)
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    if infox.author.id != int(CONFIG.BOT_ID):
        if row:
            cursor = cnx.cursor()
            sql = "SELECT * FROM response WHERE response_id = '{0}'".format(row[0])
            cursor.execute(sql)
            responses = cursor.fetchall()
            cursor.close()
            random_response = random.choice(responses)
            response_text = random_response[2]
            await infox.channel.send("{0}".format(response_text))

        cursor = cnx.cursor()
        sql = "SELECT * FROM users WHERE userid = {0} AND guild = {1}".format(infox.author.id, infox.guild.id)
        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        if row:
            new_score = int(row[2]) + 5
            cursor = cnx.cursor()
            sql = "UPDATE users SET score = {0} WHERE id = {1}".format(new_score, row[0])
            cursor.execute(sql)
            cnx.commit()
            cursor.close()
            if new_score % 100 == 0:
                rank = new_score // 100
                await infox.channel.send(">>> {0} GG, ranke {1} mobarake be mola :))".format(infox.author.mention, rank))

        else:
            cursor = cnx.cursor()
            sql = "INSERT INTO users (userid, score, guild) VALUES ({0}, {1}, {2}) ".format(infox.author.id, 0, infox.guild.id)
            cursor.execute(sql)
            cnx.commit()
            cursor.close()

    await client.process_commands(infox)


@client.command(aliases=['help', 'helps', 'helper', 'helping'])
async def command_help(infox):
    help_embed = discord.Embed(
        colour=0x0A75AD,
        title="Help ❓",
        description="Dastoorate admin ha:" \
                    "```{0}status [status]```\n```{0}activity [activity] [matn]```\n```{0}clear [meghdar]```\n```{0}mute [mention]```\n```{0}unmute [mention]```\n```{0}responses help```\n```{0}kick [mention] [reason]```\n```{0}ban [mention] [reason]```\n\nDastoorate public:\n```{0}rank```".format(CONFIG.PREFIX)
        )
    help_embed.set_footer(text='Hope you used this helps')
    help_embed.set_author(name="MahyarNV", url='http://mbehzadi.ir')
    await infox.send(embed=help_embed)


@client.command(aliases=['GG', 'Gg', 'gg', 'gG'])
async def command_gg(infox, *, pos='person'):
    await infox.send(">>> {0} you are a GG {1} ;)".format(infox.author.mention, pos))


@client.command(aliases=['status', 'setstatus', 'setst', 'set_status'])
@commands.has_permissions(administrator=True)
async def command_status(infox, status_type):
    if status_type == 'idle':
        await client.change_presence(status=discord.Status.idle)

    elif status_type == 'dnd':
        await client.change_presence(status=discord.Status.dnd)

    elif status_type == 'online':
        await client.change_presence(status=discord.Status.online)

    else:
        await infox.send(">>> {0} Status e morede nazar vojud nadarad be mola!".format(infox.author.mention))


@client.command(aliases=['activity', 'act', 'active'])
@commands.has_permissions(administrator=True)
async def command_activity(infox, act_type='', *, act_text='...'):
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
            await infox.send(">>> {0} activitie e morede nazar vojud nadarad be mola!".format(infox.author.mention))

    else:
        await infox.send(">>> {0} activitie bayad matn dashte bashe be mola!".format(infox.author.mention))


@client.command(aliases=['clear', 'cl'])
async def command_clear(infox, clear_count=0):
    if clear_count == 0:
        await infox.send("0 message nemitavanad pak shavad❌")

    else:
        await infox.channel.purge(limit=int(clear_count) + 1)
        await infox.send(">>> " + str(clear_count) + " message pak shod✔")


@client.command(aliases=['rank', 'score', 'level'])
async def command_rank(infox):
    cursor = cnx.cursor()
    sql = "SELECT * FROM users WHERE userid = {0} AND guild = {1}".format(infox.author.id, infox.guild.id)
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    if row:
        score = int(row[2])
        await infox.send(">>> {0} ranke shoma {1} ast!".format(infox.author.mention, score // 100))

    else:
        await infox.send(">>> {0} shoma leveli nadarid!".format(infox.author.mention))


@client.command(aliases=['mute', 'Mute'])
@commands.has_permissions(manage_messages=True)
async def command_mute(infox, member: discord.Member = None):
    if member:
        role = discord.utils.get(infox.guild.roles, name="Muted")
        await member.add_roles(role)
        await infox.send(">>> {0} user e morede nazar mute shod!".format(infox.author.mention))

    else:
        await infox.send(">>> {0} bayad memberi ra mention konid!".format(infox.author.mention))


@client.command(aliases=['unmute', 'Unmute', 'unMute', 'UnMute'])
@commands.has_permissions(manage_messages=True)
async def command_unmute(infox, member: discord.Member = None):
    if member:
        role = discord.utils.get(infox.guild.roles, name="Muted")
        await member.remove_roles(role)
        await infox.send(">>> {0} user e morede nazar unmute shod!".format(infox.author.mention))

    else:
        await infox.send(">>> {0} bayad memberi ra mention konid!".format(infox.author.mention))


@client.command(aliases=['response'])
@commands.has_permissions(administrator=True)
async def command_response(infox, action='', response_to='', responses=''):
    if response_to != '' and responses !='' and action !='':
        if action == 'add':
            cursor = cnx.cursor()
            sql = "SELECT * FROM responses WHERE response_to = '{0}' AND guild = {1}".format(response_to, infox.guild.id)
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

                    await infox.send(">>> {0} response add shod!".format(infox.author.mention))

                else:
                    await infox.send(">>> {0} text ba responsesh nemitune yeki bashe!".format(infox.author.mention))

            else:
                await infox.send(">>> {0} ino ghablan add dade budi, mituni deletesh koni!".format(infox.author.mention))

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
            await infox.send(">>> {0} response delete shod!".format(infox.author.mention))

        else:
            await infox.send(">>> {0} hamchin responsi sabt nashode bud!".format(infox.author.mention))

    else:
        await infox.send(">>> {0} meghdar nadadi be mola!".format(infox.author.mention))


@client.command(aliases=['responses'])
@commands.has_permissions(administrator=True)
async def command_responses(infox, *, action=''):
    if action != 'help':
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
            responses_embed.set_footer(text="shoma mitavanaid response add konid ba ']response add' (etela'te kame tar ba ]responses help)")

        responses_embed.set_author(name="MahyarNV", url='http://mbehzadi.ir')
        await infox.send(embed=responses_embed)

    else:
        help_embed = discord.Embed(
            colour=0x0A75AD,
            title="Response help ❓",
            description="""Baraye add kardane response az\n```"""+CONFIG.PREFIX+"""response add [response to] [responses]```\nestefade mikonim\n""" \
                        """Be in soorat ke jaye `[response to]` neveshte mishe `"kalame ya jomle ii ke mikhahim behesh response bedim"`\n""" \
                        """va be jaye `[responses]` neveshte mishe `"response haii ke gharare dade shavad"`\n\nhaal agar yedune response bekhaym bedim ke minevisimesh, amma age bekhaym chand ta response bedim ta be surate random har dafe yeki az aanha dade shavar, anhaa ra ba `--` az ham joda mikonim.\n mesale add kardane response:\n""" \
                        """```>response add "salam" "salam aziz--salam ✨"```\n\nbaraye delete kardane response ha:\nebteda ba `"""+CONFIG.PREFIX+"""responses` id e response e morede nazare khod ra peyda mikonim,\nSepas ba `"""+CONFIG.PREFIX+"""response delete [id]` be surati ke jaye `[id]`, id e 6 raghami ii ke copy kardim ra mizarim\nBe onvane mesal:\n```"""+CONFIG.PREFIX+"""response delete 123456```"""
            )
        help_embed.set_author(name="MahyarNV", url='http://mbehzadi.ir')
        await infox.send(embed=help_embed)


@client.command(aliases=['kick'])
@commands.has_permissions(kick_members=True)
async def command_kick(infox, member: discord.Member= None, *, reason= None):
    if not member:
        await infox.send(">>> {0} bayad memberi ra mention konid!".format(infox.author.mention))

    else:
        if not reason:
            reason = "Kick for nothing ;)!"

        await member.kick(reason= reason)
        await infox.send(">>> {0} user, kick shod".format(infox.author.mention))


@client.command(aliases=['ban'])
@commands.has_permissions(ban_members=True)
async def command_ban(infox, member: discord.Member= None, *, reason= None):
    if not member:
        await infox.send(">>> {0} bayad memberi ra mention konid!".format(infox.author.mention))

    else:
        if not reason:
            reason = "Ban for nothing ;)!"

        await member.ban(reason= reason)
        await infox.send(">>> {0} user, ban shod".format(infox.author.mention))


client.run(CONFIG.TOKEN)
