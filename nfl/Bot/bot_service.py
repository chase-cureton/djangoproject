import requests
import json
import socket
import discord

from nfl.Service import nfl_service

TOKEN = 'NTA4NzEwNTU0NzIzMDI0OTIw.DsDN4w.f8giDYGWMr0v2lGuSIyuJj9mekE'
HOST = 'https://discordapp.com/api/webhooks/508683529354477582/M8IeOwF_E25nm7tkdHuiyBRiuycbE3ByXk1kv0W3JCMDNt5e-DQb7P8spm8pkzRmPuTQ'

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!cap'):
        msg = 'Hello {0.author.mention}'.format(message)
        print(message.channel)
        print(msg)
        #await client.send_message(message.channel, msg)

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

    