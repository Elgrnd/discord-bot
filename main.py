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

    await bot.process_commands(message)

def changerUrl(message : discord.Message):
    
    if "/x." in message.content:
        url = message.content
        url = url.split("x.com")
        url[0] += "fixupx.com"
        url = url[0] + url[1]
        return url

    elif "/twitter." in message.content:
        url = message.content
        url = url.split("twitter")
        url[0] += "fixupx"
        url = url[0] + url[1]
        return url

"""
***************************************************************************************
************************** NOUVEAU MEMBRE, ASSIGNATION DE ROLES ***********************
***************************************************************************************
"""

@bot.event
async def on_member_join(member : discord.Member):
    role = discord.utils.get(member.guild.roles, id=1199720777382105160)
    await member.add_roles(role)

"""
***************************************************************************************
****************** Ajouter / Supprimer / Regarder sa date d'anniversaire **************
***************************************************************************************
"""

@bot.command()
async def anniv(ctx, date: str):
    """Ajoute la date en paramètre comme anniversaire de l'utilisateur"""
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
async def checkallanniv(ctx):
    """Liste tous les utilisateurs et leurs anniversaires."""
    
    if ctx.channel.id != 1341520022194884669:
        return

    await ctx.message.delete()

    if not birthdays:
        await ctx.send("❌ Il n'y a aucun anniversaire enregistré.")
        return
    
    # Crée une liste formatée des anniversaires
    all_birthdays = ""
    for user_id, date in birthdays.items():
        member = ctx.guild.get_member(int(user_id))
        if member:
            all_birthdays += f"{member} : {date}\n"
        else:
            all_birthdays += f"[Membre introuvable] {user_id} : {date}\n"

    await ctx.send(f"🎉 **Liste des anniversaires :**\n{all_birthdays}")

@bot.command()
async def delanniv(ctx):
    """Supprime son propre anniversaire"""
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

    # Recharge les anniversaires depuis le fichier JSON
    try:
        with open(birthdays_file_path, "r") as file:
            loaded_birthdays = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        loaded_birthdays = {}

    today = datetime.today().strftime("%d/%m")

    for user_id, birth_date in loaded_birthdays.items():
        if birth_date == today:
            user = await bot.fetch_user(int(user_id))
            if user:
                channel = discord.utils.get(bot.get_all_channels(), id=1341520022194884669)
                if channel:
                    message = await channel.send(f"🎂 Joyeux anniversaire {user.mention} ! 🥳🎉 @everyone")
                    await message.add_reaction("🎉")
                    await message.add_reaction("🥳")

"""
***************************************************************************************
************************** Clear channel **********************************************
***************************************************************************************
"""

@bot.command()
async def clear(ctx):
    
    if ctx.author.id == 736602549066661889:
        await ctx.channel.purge()
        await ctx.send("`✅ Salon nettoyé`")
    else:
        await ctx.message.delete()
        await ctx.send("`❌ Tu n'as pas les droits !`")

@bot.command()
async def like(ctx, emoji: str):
    # Vérifie que c’est une réponse à un autre message
    if ctx.message.reference:
        try:
            # Récupère le message auquel tu as répondu
            referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if emoji == None:
                await ctx.message.add_reaction("❤️")
            else:
                # Tente d'ajouter l'emoji en réaction
                await referenced_message.add_reaction(emoji)
            await ctx.message.add_reaction("✅")  # Confirmation visuelle
        except discord.HTTPException:
            await ctx.send("❌ L'emoji est invalide ou je ne peux pas l'utiliser.")
        except Exception as e:
            await ctx.send(f"Erreur : {e}")
    else:
        await ctx.send("❗ Réponds à un message avec `+like <emoji>` pour que je l'utilise en réaction.")

    

if __name__ == '__main__':
    load_dotenv()
    clientId = os.getenv("clientId")
    bot.run(clientId)
