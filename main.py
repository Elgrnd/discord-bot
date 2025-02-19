import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import os
import json
import asyncio
from datetime import datetime

bot = commands.Bot(command_prefix='+', intents=discord.Intents.all())
persistent_dir = "/mnt/data"
birthdays_file_path = os.path.join(persistent_dir, "birthdays.json")

# Chargement des anniversaires enregistrés
try:
    with open(birthdays_file_path, "r") as file:
        birthdays = json.load(file)
except FileNotFoundError:
    birthdays = {}
"""
***************************************************************************************
****************** AFFICHE SI LE BOT EST EN LIGNE ET SUR QUELS SERVEURS ***************
***************************************************************************************
"""

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready")
    for server in bot.guilds:
        print(f'{server.name}(id: {server.id})')
    #client.loop.create_task(checkTime())
    check_birthdays.start()

"""
***************************************************************************************
************************** MODIFICATION DE LIEN TWITTER ET X **************************
***************************************************************************************
"""

@bot.event
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

@bot.event
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

"""
***************************************************************************************
************************** Ajouter sa date d'anniversaire *************************
***************************************************************************************
"""

@bot.command()
async def anniv(ctx, date: str):

    if ctx.channel.id != 1341520022194884669:
        return
    
    await ctx.message.delete()

    """Ajoute l'anniversaire de l'utilisateur (format: JJ/MM)."""
    user_id = str(ctx.author.id)
    
    try:
        datetime.strptime(date, "%d/%m")
        if user_id in birthdays:
            await ctx.send(f"{ctx.author.mention}, ton anniversaire est déjà entré !")
            return
        birthdays[user_id] = date

        with open(birthdays_file_path, "w") as file:
            json.dump(birthdays, file)

        await ctx.send(f"🎉 {ctx.author.mention}, ton anniversaire est enregistré pour le {date} !")
    except ValueError:
        await ctx.send("Format invalide ! Utilise : `+anniv JJ/MM`")

@bot.command()
async def checkanniv(ctx, member: discord.Member = None):
    """Vérifie si l'utilisateur ou un autre membre a enregistré son anniversaire."""

    if ctx.channel.id != 1341520022194884669:
        return

    await ctx.message.delete()

    # Si aucun membre n'est précisé, on utilise l'auteur du message
    member = member or ctx.author
    user_id = str(member.id)

    if user_id in birthdays:
        date = birthdays[user_id]
        await ctx.send(f"🎉 {member}, l'anniversaire est enregistré pour le {date}.")
    else:
        await ctx.send(f"❌ {member} n'a pas d'anniversaire enregistré.")


@bot.command()
async def delanniv(ctx):

    if ctx.channel.id != 1341520022194884669:
        return
    
    await ctx.message.delete()

    """Supprime l'anniversaire de l'utilisateur."""
    user_id = str(ctx.author.id)

    if user_id in birthdays:
        del birthdays[user_id]
        with open(birthdays_file_path, "w") as file:
            json.dump(birthdays, file)
        await ctx.send(f"🎉 L'anniversaire de {ctx.author.mention} a été supprimé !")
    else:
        await ctx.send(f"❌ {ctx.author.mention}, tu n'as pas d'anniversaire enregistré.")

"""
***************************************************************************************
************************** Afficherl'anniversaire *************************************
***************************************************************************************
"""

@tasks.loop(hours=24)
async def check_birthdays():
    """Vérifie chaque jour si c'est l'anniversaire d'un utilisateur et envoie un message."""
    await bot.wait_until_ready()
    today = datetime.today().strftime("%d/%m")

    for user_id, birth_date in birthdays.items():
        if birth_date == today:
            user = await bot.fetch_user(int(user_id))
            if user:
                channel = discord.utils.get(bot.get_all_channels(), id=1341520022194884669)
                if channel:
                    await channel.send(f"🎂 Joyeux anniversaire {user.mention} ! 🥳🎉 @everyone")


if __name__ == '__main__':
    load_dotenv()
    clientId = os.getenv("clientId")
    bot.run(clientId)