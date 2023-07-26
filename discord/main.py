import discord
from discord.ext import commands
import shutil
import datetime
import os
import requests
import uuid
import pathlib
import zlib


# set bot prefix
bot_prefix = "!"

# make instance from Bot class
bot = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.all())


# make bot ready
@bot.event
# starting Bot
async def on_ready():
    """this a function for make bot ready"""
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}\n{30*"_"}\n')

# a test command
@bot.command()
async def hello(ctx):
    """this a test command for testing bot"""
    await ctx.send("Hi, i'm a discord bot!")


# totem command
@bot.command()
async def totem(ctx):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url.startswith("https://cdn.discordapp.com"):           
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                now = datetime.datetime.now()
                year = now.year
                month = now.month
                day = now.day
                hour = now.hour
                minute = now.minute
                second = now.second

                destination_path = os.path.join("exports", f"{year}", f"{month}", f"{day}", f"{hour}", f"{minute}", f"{second}")
                src = os.path.join(os.getcwd(), "src")
                print(src)
                os.makedirs(destination_path, exist_ok=True)

                if os.path.exists(destination_path):
                    shutil.rmtree(destination_path)

                shutil.copytree(src, destination_path)
                file_name = os.path.join(destination_path, "assets", "minecraft", "textures", "item", "totem_of_undying.png")
            
                with open(file_name, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)

                zip_name = os.path.join(os.path.join("final exports", f"export-{year}-{month}-{day}-{hour}-{minute}-{second}"))
                print(zip_name)
                

                # file=discord.File(zip_name)
                await ctx.send(file=discord.File(shutil.make_archive(zip_name, 'zip', destination_path)))

            else:
                await ctx.send("Error: Failed to fetch the image! please try again")
        else:
            await ctx.send("Invalid image link!")

@bot.command()
async def showHelp(ctx):
    with open("help.md", "r", encoding="utf-8") as file:
        help_text = file.read()
    await ctx.send(help_text)
 


# connecting bot to discord servers
bot.run('token')