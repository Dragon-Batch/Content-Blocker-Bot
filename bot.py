import json, time
import threading
import discord, os, traceback
from discord.ext import commands

with open("config.json", "r", encoding = "utf-8") as f: config = json.load(f)

client = commands.Bot('!', intents = discord.Intents.all())

client.blacklisted_links = []
with open("blacklist.json", "r", encoding = "utf-8") as f:
    client.blacklisted_links = json.load(f)["blacklisted_links"]

def update_blacklist():
    saved = client.blacklisted_links.copy()

    while True:
        time.sleep(1)

        if saved != (unsaved := client.blacklisted_links.copy()):
            saved = unsaved

            with open("blacklist.json", "w", encoding = "utf-8") as f:
                json.dump({"blacklisted_links": saved}, f)

threading.Thread(target = update_blacklist).start()

@client.event
async def on_ready():
    print("Bot Ready!")

unloaded_cogs: list[str] = []
loaded_cogs: list[str] = []

for file_name in os.listdir("Cogs/"):
    if file_name.startswith("_"): continue
    unloaded_cogs.append('.'.join(file_name.split(".")[:-1]))

@client.command(aliases = ['lc'])
@commands.is_owner()
async def load(ctx: commands.Context):
    global unloaded_cogs

    cogs = unloaded_cogs.copy()
    unloaded_cogs = []

    for cog in cogs.copy():
        try:
            client.load_extension("Cogs." + cog)
            loaded_cogs.append(cog)

        except Exception as error:
            traceback.print_exception(error)
            cogs.remove(cog)
            unloaded_cogs.append(cog)

    if cogs == []: return
    await ctx.send(f"loaded ``{', '.join(cogs)}``")

@client.command(aliases = ['uc'])
@commands.is_owner()
async def unload(ctx: commands.Context):
    global loaded_cogs

    cogs = loaded_cogs.copy()
    loaded_cogs = []

    for cog in cogs.copy():
        try:
            client.unload_extension("Cogs." + cog)
            unloaded_cogs.append(cog)
        except Exception as error:
            traceback.print_exception(error)
            cogs.remove(cog)
            loaded_cogs.append(cog)

    if cogs == []: return
    await ctx.send(f"unloaded ``{', '.join(cogs)}``")

client.run(config["token"])