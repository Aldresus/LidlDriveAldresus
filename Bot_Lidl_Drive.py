import discord
from discord.ext import commands
import datetime
import smtplib
from email.message import EmailMessage

login="Mot de passe du compte GMail"
user="Adresse mail du compte GMail"




def embed(ctx):
    embed=discord.Embed(title="**Aide:**", color=0xfcf794)
    embed.set_author(name="Lidl Drive")
    embed.add_field(name="**!drive [pseudo minecraft] [quantité] [nom de l'item]** ", value="Commande pour utiliser le service Lidl Drive.")
    embed.add_field(name="**!historique**", value="Commande pour afficher l'historique des commandes de l'utilisateur.")
    embed.set_footer(text="Made by Aldresus with <3")
    embed.set_image(url="https://cdn.discordapp.com/attachments/542050063623520258/727880766062723082/favicon.png")
    return embed

description = "Un bot conçu pour le service Lidl Drive."
client = commands.Bot(command_prefix='!', description=description)
joueA="!drive pour passer commande !"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name=joueA))

@client.command()
async def aide(ctx):
    await ctx.send(embed=embed(ctx),delete_after=20)

@client.command()
async def drive(ctx, pseudo:str, quantite, item):
    pseudoDiscord=ctx.message.author
    reception=client.get_user("ID de la personne qui doit recevoir les commandes")
    await ctx.message.delete()
    await ctx.send("> Votre commande à été enregistrée !",delete_after=4)
    commande="{0} --> **@{1}** ( {2} ) à commandé **{3}** de **{4}**\n".format(datetime.datetime.now().strftime("%d - %m - %Y"),pseudoDiscord,pseudo,quantite,item)
    await reception.send(commande)
    idDiscord=ctx.message.author.id
    await client.get_user(idDiscord).send("Merci pour votre commande de {0} de {1}, celle-ci serat traitée dans les plus brefs délais !".format(quantite,item))
    #écriture dans le fichier qui sert de logs
    f=open("historique.txt","a")
    f.write(commande.replace("*",""))
    f.close
    #envoi du mail.
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        to = 'Adresse mail du destinataire'
        subject = 'Nouvelle commande Lidl Drive !'
        body = "Une nouvelle commande vient d'arriver le {0} !\nNom en jeu : {1}\nNom discord : @{2}\nItem : {3} de {4}".format(datetime.datetime.now().strftime("%d - %m - %Y"),pseudo,pseudoDiscord,quantite,item)
        server.login(user, login)
        message=EmailMessage()
        message.set_content(body)
        message['Subject']=subject
        message['From']=user
        message['To']=to

        server.send_message(message)
        server.close()
    except:
        await ctx.send("Une erreure est survenue ! **Patientez ou contactez un admin** !")

@drive.error
async def drive_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete(delete_after=3)
        await ctx.send("> Vous devez entrer tout les arguments !",delete_after=10)
        await ctx.send(embed=embed(ctx),delete_after=20)
    else: raise error

@client.command()
async def historique(ctx):
    ctx.message.delete()
    ctx.send("Votre historique vient de vous être envoyé en message privé !",delete_after=4)
    idPseudoDiscord=ctx.message.author.id
    print(idPseudoDiscord)
    pseudoDiscord=ctx.message.author.name
    print(pseudoDiscord)
    historiqueJoli=""
    f = open("historique.txt","r")
    historique=[]
    lignes=f.readlines()
    f.close

    for i in lignes:
        print("i:",i)
        if pseudoDiscord in i:
            historique.append(i)

    print("l'historique est:",historique)

    antiSpamHistorique=[]
    if historique==[]:
        await ctx.send("**Vous n'avez encore rien commandé !**")
    else:
        await ctx.send("------------------------------------------------")
        await ctx.send("Voici l'historique de vos commandes :")
        #petit algo pour contourner le nombre max de caraactère de Discord
        for i in historique:
            antiSpamHistorique.append(i)
            if len(antiSpamHistorique) > 3: #j'affiche uniquement les parties de l'historiques 3 par 3 pour éviter l'antiSpam
                historiqueJoli=historiqueJoli.join(antiSpamHistorique)
                await ctx.send(historiqueJoli)
                antiSpamHistorique.clear()
                historiqueJoli=""

        historiqueJoli=historiqueJoli.join(antiSpamHistorique)
        await ctx.send(historiqueJoli)
        await ctx.send("Merci de votre fidélité ! ( :")
        await ctx.send("------------------------------------------------")
    antiSpamHistorique.clear()
    historiqueJoli=""

client.run('Token du bot')