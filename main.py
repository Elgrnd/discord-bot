import discord
from dotenv import load_dotenv
import os
from datetime import datetime
from datetime import datetime, timedelta

client = discord.Client(intents=discord.Intents.all())

"""
***************************************************************************************
****************** AFFICHE SI LE BOT EST EN LIGNE ET SUR QUELS SERVEURS ***************
***************************************************************************************
"""

@client.event
async def on_ready():
    print(f"{client.user.name} is ready")
    for server in client.guilds:
        print(f'{server.name}(id: {server.id})')
    #client.loop.create_task(checkTime())

"""
***************************************************************************************
************************** MODIFICATION DE LIEN TWITTER ET X **************************
***************************************************************************************
"""

@client.event
async def on_message(message : discord.Message):
    if message.author.bot:
        return
    
    if "/x." in message.content or "/twitter." in message.content:
        await message.delete()
        message_return = changerUrl(message)
        await message.channel.send(f"{message.author.mention} le goat a drop ce tweet zinzin : {message_return}")
        print(message.author, datetime.now)

def changerUrl(message : discord.Message):
    url = []
    lien = ""
    for char in message.content:
        url.append(char)
    
    if "/x." in message.content:
        for i in range(len(url) - 1):
            if url[i] == "x":
                url[i] = "vxtwitter"
                break

        for i in range(len(url) - 1):
            lien += url[i]

        return lien 

    elif "/twitter." in message.content:
        url = message.content
        url = url.split("twitter")
        url[0] += "vxtwitter"
        url = url[0] + url[1]
        return url

"""
***************************************************************************************
************************** NOUVEAU MEMBRE, ASSIGNATION DE ROLES ***********************
***************************************************************************************
"""

@client.event
async def on_member_join(member : discord.member):
    role = discord.utils.get(member.guild.roles, id=1199720777382105160)
    await member.add_roles(role)

"""
***************************************************************************************
************************** ENVOYER MESSAGE LOL TOUS LES JOURS *************************
***************************************************************************************
"""

"""
async def send_daily_message():
    # Obtient l'objet canal en fonction de l'ID
    channel = client.get_channel(1199722180976590969)
    
    if channel is not None:
        # Envoie le message
        await channel.send(f"__**League Of Legends**__\n\n`Qui 5v5 ce soir ?` <@&1201581459580923905> \n\n\t> Présent → `🟢`\n\t> Absent → `🔴`\n\n*Donnez une heure aussi :clock1: *")
"""
'''

@client.event
async def checkTime():
    while True:
        # Récupère l'heure actuelle
        now = datetime.now()
        # Définit l'heure à laquelle le message doit être envoyé (16h)
        target_time = now.replace(hour=16, minute=00, second=00, microsecond=0)
        # Si l'heure actuelle est supérieure ou égale à l'heure cible, calcule l'heure pour le lendemain
        if now >= target_time:
            target_time += timedelta(days=1)
        # Calcule la différence de temps jusqu'à l'heure cible
        delta = target_time - now
        # Attendez jusqu'à l'heure cible pour envoyer le message
        await asyncio.sleep(delta.total_seconds())
        # Envoyer le message quotidien
        await send_daily_message()
'''



if __name__ == '__main__':
    load_dotenv()
    clientId = os.getenv("clientId")
    client.run(clientId)