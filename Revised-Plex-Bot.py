'''
I made this revision to the code as a more user friendly approch for those who dont want to use dockers and such. 
Make sure you update the file paths, and everything in the "Fill This Out"
This should work without any other requirments. 
'''


import discord
import random
import requests
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from plexapi.video import Movie, Video
from plexapi.server import PlexServer
from plexapi.mixins import PosterUrlMixin
#_________________________________Fill This Out_________________________________________#
# Prerequisites
# pip install discord-py-slash-command==3.0.1a0
# pip install discord.py==1.7.3

#Be sure to update the file paths in code accordingly. 

#web address to Plex server e.g., http://192.168.1.19:32400
baseurl = 'LOCAL_IP_HERE'

#Plex token. See: https://www.plexopedia.com/plex-media-server/general/plex-token/
plextoken = 'PLEX_TOKEN_HERE'

#Discord bot token.
discordtoken = "DISCORD_BOT_TOKEN_HERE"

#To get system(below), run the bot with the above filled out. In the console it'll print out avalable clients to connect to.
#After first run, stop the bot and place the client in the system = field.
system = "SYSTEM_ID_HERE"



#Add the voice channel ID to connect to.
voicechannel = VOICE_CHANNEL_ID_HERE
#________________________________________________________________________________________#
plex = PlexServer(baseurl, plextoken)

Bot_Prefix = "!"
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=Bot_Prefix, case_insensitive=True, self_bot=False, HelpCommand=False, intents=intents)
slash = SlashCommand(bot, sync_commands=True)

print("|_____________Available clients on local network_____________|")
clients = []
for client in plex.clients():
    clients.append(client.title)
    print(f"| •Name: \033[4m{client.title}\033[0m ({client.product})")
print("|____________________________________________________________|")

if clients[0] != system:
    print(f"{system} doesn't apper to be online. Quitting. ⛔")
    quit()
else:
    print(f"{system} online. ✔️")

movielist = []
movies = plex.library.section('Movies')
for video in movies.search():
    movielist.append('%s' % (video.title))
moviecount = len(movielist)
print(f"Loaded {moviecount} Movies. ✔️")

p = 0
r = 0


@slash.slash(name="Ajuda", description="Mostra o menu de ajuda.")
async def ajuda(ctx):
    embed = discord.Embed(title="Ajuda", description=" ", color=0xf5dd03)
    embed.add_field(name="``/pesquisar <pesquisa>``", value="```fix\nPesquisa um filme.```", inline=False)
    embed.add_field(name="``/info <filme>``", value="```fix\nObtém informações de um filme.```", inline=False)
    embed.add_field(name="``/assistir <filme>``",value="```fix\nComeçar a assistir um filme.```",inline=False)
    embed.add_field(name="``/aleatorio``",value="```fix\nAssistir um filme aleatório.```",inline=False)
    embed.add_field(name="``/pausar``",value="```fix\nPausa o filme atual.```",inline=False)
    embed.add_field(name="``/despausar``", value="```fix\nDespausa o filme atual.```", inline=False)
    embed.add_field(name="``/parar``", value="```fix\nPara o filme atual.```", inline=False)
    await ctx.send(embed=embed)


@slash.slash(name="Pesquisar", description="Pesquisa um filme.")
async def search(ctx, *, pesquisa):
    movie = []
    movies = plex.library.section('Movies')
    try:
        for video in movies.search(keyword):
            movie.append('%s' % (video.title))
        results = ('\n •'.join(movie))
        if movie == []:
            results = "Nenhum filme encontrado!"
        embed = discord.Embed(title=f"__Resultados da pesquisa:__", description=f"•{results}", color=0xf5dd03)
        embed.set_footer(text=f"Pesquisa: {keyword}")
        await ctx.send(embed=embed)
    except:
        await ctx.send("Erro!!")


@slash.slash(name="Info", description="Obtém informações de um filme.")
async def info(ctx, *, filme):
    try:
        play = plex.library.section('Movies').get(filme)
        client = plex.client(system)
        client.proxyThroughServer()
        image = PosterUrlMixin.thumbUrl.fget(play)
        img_data = requests.get(image).content
        with open('movie.jpg', 'wb') as handler:
            handler.write(img_data)
        duration = int(play.duration / 60000)
        embed = discord.Embed(title=f"Infor For: {filme}", description=f"{play.summary}\n\n**Classificação Rotten Tomatoes:** {play.audienceRating}\n**Classificação de conteúdo:** {play.contentRating}\n**Duração:** {duration} minutos", color=0xf5dd03)
        file = discord.File("C:/Users\conta\Desktop\Bots\PlexBot\movie.jpg", filename="movie.jpg")
        embed.set_image(url="attachment://movie.jpg")
        embed.set_footer(text=f"{play.year} - {play.studio}")
        await ctx.send(file=file, embed=embed)
    except:
        embed = discord.Embed(title=f"I couldn't find: {filme}.", description="Filme não encontrado. Use o /pesquisar para obter o nome correto do filme.", color=0xf5dd03)
        await ctx.send(embed=embed)


@slash.slash(name="assistir", description="Assiste um filme.")
async def assistir(ctx, *, filme):
    try:
        global currentlyplaying
        global savemovietitle
        savemovietitle=filme
        play = plex.library.section('Movies').get(filme)
        client = plex.client(system)
        client.proxyThroughServer()
        client.playMedia(play)
        client.setParameters(volume=100, shuffle=0, repeat=0)
        image = PosterUrlMixin.thumbUrl.fget(play)
        img_data = requests.get(image).content
        with open('movie.jpg', 'wb') as handler:
            handler.write(img_data)
        duration = int(play.duration / 60000)
        embed = discord.Embed(title=f"Assistindo: {filme}", description=f"{play.summary}\n\n**Classificação Rotten Tomatoes:** {play.audienceRating}\n**Classificação de conteúdo:** {play.contentRating}\n**Duração:** {duration} minutos", color=0xf5dd03)
        file = discord.File("C:/Users\conta\Desktop\Bots\PlexBot\movie.jpg", filename="movie.jpg")
        embed.set_image(url="attachment://movie.jpg")
        embed.set_footer(text=f"{play.year} - {play.studio}")
        await ctx.send(file=file, embed=embed)
    except:
        embed = discord.Embed(title=f"I couldn't find: {filme}.", description="If you're having trouble, use /search to search for the movie then copy and paste (punctuation matters).", color=0xf5dd03)
        await ctx.send(embed=embed)


@slash.slash(name="Parar", description="Para o filme atual.")
async def parar(ctx):
    global savemovietitle
    currentlyplaying = plex.sessions()
    if currentlyplaying == []:
        embed = discord.Embed(title=f"Ops!", description="Nenhum filme está sendo exibido.", color=0xf5dd03)
        await ctx.send(embed=embed)
    else:
        client = plex.client(system)
        client.proxyThroughServer()
        client.stop()
        embed = discord.Embed(title=f"__Parou de tocar__:", description=f"{savemovietitle}", color=0xf5dd03)
        await ctx.send(embed=embed)


@slash.slash(name="Pausar", description="Pausa o filme atual.")
async def pausar(ctx):
    global savemovietitle
    currentlyplaying = plex.sessions()
    if p==1:
        embed = discord.Embed(title=f"Ops!", description=f"{savemovietitle} já está pausado.", color=0xf5dd03)
        await ctx.send(embed=embed)
    else:
        client = plex.client(system)
        client.proxyThroughServer()
        client.pause()
        embed = discord.Embed(title=f"__Pausado__:", description=f"{savemovietitle}", color=0xf5dd03)
        await ctx.send(embed=embed)


@slash.slash(name="Despausar", description="Despausa o filme.")
async def despausar(ctx):
    global savemovietitle
    currentlyplaying = plex.sessions()
    if r==1:
        embed = discord.Embed(title=f"Ops!", description=f"{savemovietitle} já está tocando.", color=0xf5dd03)
        await ctx.send(embed=embed)
    else:
        client = plex.client(system)
        client.proxyThroughServer()
        client.play()
        embed = discord.Embed(title=f"__Despausado__:", description=f"{savemovietitle}", color=0xf5dd03)
        await ctx.send(embed=embed)


@slash.slash(name="Aleatorio", description="Toca um filme aleatório. Por favor espere...")
async def aleatorio(ctx):
    global currentlyplaying
    global savemovietitle
    rc = random.choice(movielist)
    savemovietitle = rc
    play = plex.library.section('Movies').get(rc)
    client = plex.client(system)
    client.proxyThroughServer()
    client.playMedia(play)
    client.setParameters(volume=100,shuffle=0,repeat=0)
    image = PosterUrlMixin.thumbUrl.fget(play)
    img_data = requests.get(image).content
    with open('movie.jpg', 'wb') as handler:
        handler.write(img_data)
    duration = int(play.duration / 60000)
    embed = discord.Embed(title=f"**Assistindo:** {rc}", description=f"{play.summary}\n\n**Classificação Rotten Tomatoes:** {play.audienceRating}\n**Classificação de conteúdo:** {play.contentRating}\n**Duração:** {duration} minutos" ,color=0xf5dd03)
    file = discord.File("C:/Users\conta\Desktop\Bots\PlexBot\movie.jpg", filename="movie.jpg")
    embed.set_image(url="attachment://movie.jpg")
    embed.set_footer(text=f"{play.year} - {play.studio}")
    await ctx.send(file=file, embed=embed)
    playtime = int(play.duration / 1000)


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    channel = bot.get_channel(voicechannel)
    print(bot.user, 'is online. ✔️')
    print(f"Connected to voice channel: {channel.name} ✔️")
    await channel.connect()


bot.run(discordtoken, bot=True, reconnect=True)
