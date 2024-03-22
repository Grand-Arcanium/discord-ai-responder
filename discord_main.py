"""
This is a simple script to put the Chat GPT bot code online as a discord bot.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 1.0
"""
import discord
import regex as re
from config import get_discord_token
from responder import *

class MyClient(discord.Client):
    """
    A Class to represent the Client (bot user)

    @param discord.Client: the client connection to the bot user
    """

    def __init__(self):
        """
        CONSTRUCTOR: Sets the default 'intents' for the bot.

        @param self: this bot client
        """

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """
        Called when the bot is fully logged in.

        @param self: this bot client
        """
        print('Logged on as', self.user)

    async def on_message(self, message):
        """
        Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information.

        @param self: this bot client
        @param message: contains all the information related to the message
        """

        # don't respond to ourselves
        if message.author == self.user:
            return

        # check if mentioned
        if self.user in message.mentions:

            # get the user that mentioned the bot
            mention = message.author.mention

            # get the utterance and generate the response
            utterance = re.sub(r'<@.*>', '', message.content).strip() # remove the mention
            # utterance = message.content # <- doesn't remove the mention

            if utterance.lower().find('hello') >= 0: # default greeting response
                response = "".join(['Hello, ', mention, '!'])
            else: # all other responses
                intent = understand(utterance)
                response = "".join([mention, " ", generate(intent)])

            # send the response
            await message.channel.send(response)

            # check message
            global msg
            msg = message
            print(message)


## Set up and log in
client = MyClient()
bot_token = get_discord_token()
with open(bot_token) as file:
    token = file.read()
client.run(token)