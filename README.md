# Setup
1. download [Python 3.10.1](https://www.python.org/downloads/release/python-3101/)
2. run it (not as administrator)
3. select "Customize Installation"
4. select "Documentation", "pip", "td/tk and IDLE", "Python test suite", "py launcher"
5. unselect everything else
6. press next
7. select "Associate files with Python", "Create shortcuts for installed applications"
8. unselect everything else
9. install

# Configuration
1. create a [Discord Bot](https://discord.com/developers/applications)
2. once created, goto the "Bot" tab on the left of the page
3. click "Reset Token" and then press the `copy` button
4. open config.json and replace `YOUR BOT TOKEN HERE` with your bot token
5. scroll down on the bot tab under "Privileged Gateway Intents", select "PRESENCE INTENT", "SERVER MEMBERS INTENT" and "MESSAGE CONTENT INTENT"
6. Save Changes
7. open notepad
8. copy and paste discord.com/api/oauth2/authorize?client_id=``YOUR BOT ID``&permissions=274878000128&scope=bot into it
9. goto the "General Information" tab and copy your "APPLICATION ID"
10. replace "YOUR BOT ID" in the notepad with your APPLICATION ID
11. goto that link to add the bot to your server

## Optional (Recommended)
### You can unselect "PUBLIC BOT" to make the bot so no one exept you can add it

# Startup
1. double click "bot.py"
2. your done :)))))

# Commands

``!blacklist``
reply to a message with this command to blacklist all links

``!unblacklist [link]``
unblacklist a specific link

``!load``
loads the Blacklist.py cog

``!unload``
Unloads the Blacklist.py cog