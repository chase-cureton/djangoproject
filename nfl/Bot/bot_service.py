import requests
import json
import socket
import discord
import os, types

from nfl.Service import nfl_service

TOKEN = 'NTA4NzEwNTU0NzIzMDI0OTIw.DsDN4w.f8giDYGWMr0v2lGuSIyuJj9mekE'
HOST = 'https://discordapp.com/api/webhooks/508683529354477582/M8IeOwF_E25nm7tkdHuiyBRiuycbE3ByXk1kv0W3JCMDNt5e-DQb7P8spm8pkzRmPuTQ'

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('*hello cap'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('*top'):
        init, count, pos, week_identifier, week = message.content.split(" ")
        print("Action: ", init)
        print("Count: ", count)
        print("Position: ", pos)

        count = int(count)
        if not isinstance(count, int): 
            print('Come on now, you gotta enter a limit!')
            return

        if week_identifier != 'week' and week_identifier != 'Week':
            print('What are you thinking?!')
            return

        print("Week: ", week)

        stats = nfl_service.GetTopPlayers(stat_type=pos, count=count, week=week)

        if 'rec' in pos:
            i = 0
            message_list = []
            for player_stats in stats:
                i+=1
                new_row = '%d.) %s - Rec Yards: %s' % (i, player_stats.player.shortName, player_stats.rec_yards)
                message_list.append(new_row)
            
            response = '\n'.join(message_list)
            await client.send_message(message.channel, response)

        if 'pass' in pos:
            i = 0
            message_list = []
            for player_stats in stats:
                i+=1
                new_row = '%d.) %s - Pass Yards: %s' % (i, player_stats.player.shortName, player_stats.pass_yards)
                message_list.append(new_row)
            
            response = '\n'.join(message_list)
            await client.send_message(message.channel, response)

        if 'rush' in pos:
            i = 0
            message_list = []
            for player_stats in stats:
                i+=1
                new_row = '%d.) %s - Rush Yards: %s' % (i, player_stats.player.shortName, player_stats.rush_yards)
                message_list.append(new_row)
            
            response = '\n'.join(message_list)
            await client.send_message(message.channel, response)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----------')

def bot_listen():
    client.run(TOKEN)

def webhook_post_discord(message="default test message"):
    post_dto = {
        'username': 'Captain Hook',
        'content': message
    }

    r = requests.get(allow_redirects=False, url=HOST)
    print (r.text)

    r = requests.post(url=HOST, json=post_dto)
    print (r.text)

    