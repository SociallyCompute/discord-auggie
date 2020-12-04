import discord
from discord.ext import commands
import requests
import csv
import subprocess
from subprocess import Popen, PIPE

client = commands.Bot(command_prefix = '-')
client.remove_command('help')

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))


@client.command()
async def add(ctx, repo):
    
    with open("csv_file.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        line = "1" + repo
        csvwriter.writerow(line.split())

    try:
        subprocess.call(["augur", "db", "add-repos", "csv_file.csv"])
    except:
        print("didnt work")
    finally:
        print("it worked")
    
    response = requests.get("http://localhost:5114/api/unstable/repos/22071/laborhours")
    print(response.status_code)

@client.command()
async def list(ctx):

    try:
        p = Popen(["augur", "db", "get-repo-groups"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    except:
        print("didnt work")
    finally:
        print("it worked")
    
    repo_tuple = p.communicate()
    
    await ctx.send(repo_tuple)

@client.command()
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.red()
    )

    embed.set_author(name='Help')
    embed.add_field(name='-request-data <repo link>', value='Gives back data about repo by providing link to repo', inline=False)
    embed.add_field(name='-add-repo <repo link>', value='Adds repo to our repo database that the bot will regularly check to provide updates', inline=False)
    embed.add_field(name='-schedule <frequency>', value='Specify scheduled message time. Options are: daily, weekly, or monthly', inline=False)
    embed.add_field(name='-list', value='Returns list of repos you are following', inline=False)
    
    await ctx.author.send(author, embed=embed)

client.run('Nzc5MTI0NjM0MzE4NTM2NzM1.X7b-XA.oRXK0UVSUOtTdXZLsbogC0i4ZJY')
