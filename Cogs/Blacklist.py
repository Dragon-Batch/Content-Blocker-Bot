import re
import time
import discord
from discord.ext import commands

url_pattern = r'https?://\S+'
rate_limits: dict[str, dict[str, float]] = {}

def ratelimit_action(user: int, action: str, timelimit: float):
    """will return True if you are not rate limited."""

    if not user in rate_limits:
        rate_limits[user] = {action: time.time()}
        return True

    if not action in rate_limits[user]:
        rate_limits[user][action] = time.time()
        return True

    if (time.time() - rate_limits[user][action]) > timelimit:
        rate_limits[user][action] = time.time()
        return True

    return False

class Blacklist(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_load(self):
        print("Blacklist Cog Loaded!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        links = re.findall(url_pattern, message.content)
        for link in self.client.blacklisted_links.copy():
            if link in links:
                if ratelimit_action(message.author.id, "blacklisted-link-warning", 10):
                    await message.channel.send(f"Please do **NOT** send that link! {message.author.mention}")
                await message.delete(reason = f"{message.author.id} sent a blacklisted link")
                return

    @commands.command(description = "Reply to a message with this command to blacklist all links.")
    @commands.has_permissions(manage_messages = True)
    async def blacklist(self, ctx: commands.Context):
        if ctx.message.reference is None:
            await ctx.reply("You need to execute this command while replying to a message.")
            return

        print(ctx.message.reference.message_id)
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        links = re.findall(url_pattern, message.content)

        if not links:
            await ctx.send("there are no links in this message.")
            return

        for link in links.copy():
            if link in links.copy() and link in self.client.blacklisted_links:
                links.remove(link)

        if not links:
            await ctx.send("there are no links in this message that are not blacklisted.")
            return

        self.client.blacklisted_links.extend(links)

        embed = discord.Embed(title = "Blacklisted")
        embed.description = """
        **I have blacklisted:**\n\n""" + '\n'.join(links)
        embed.set_footer(text = "unblacklist a link with:  !unblacklist [link]")
        await ctx.send(embed = embed)

    @commands.command(description = "Unblacklist links with this command.")
    @commands.has_permissions(manage_messages = True)
    async def unblacklist(self, ctx: commands.Context, urls: str = ""):
        links = re.findall(url_pattern, urls)

        if not links:
            await ctx.send("you did not give any links.")
            return

        for link in links.copy():
            if link in links.copy() and not link in self.client.blacklisted_links:
                links.remove(link)

        if not links:
            await ctx.send("link(s) not blacklisted")
            return

        for link in links:
            self.client.blacklisted_links.remove(link)

        embed = discord.Embed(title = "Unblacklisted")
        embed.description = """
        **I have unblacklisted:**\n\n""" + '\n'.join(links)
        await ctx.send(embed = embed)

def setup(client: commands.Bot):
    client.add_cog(Blacklist(client))