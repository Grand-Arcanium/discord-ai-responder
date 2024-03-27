"""
This is a simple script to put the Chat GPT bot code online as a discord bot.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 1.0
"""
import discord
from config import get_discord_token
from responder import *
import regex as re
from dataHandler import *

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
        create_server_memory(self.guilds)
        print('Logged on as', self.user)
        print('God save the queen!')

    async def on_message(self, message):
        """
        Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information.

        @param self: this bot client
        @param message: contains all the information related to the message
        """

        # don't respond to ourselves

        if message.author == self.user or message.author.bot:
            return

        # check if mentioned
        if self.user in message.mentions:

            # get the user that mentioned the bot
            global responding
            mention = message.author.mention

            # get the utterance and generate the response
            utterance = re.sub(r'<@.*>', '', message.content).strip()  # remove the mention
            # utterance = message.content # <- doesn't remove the mention

            response = ''
            if utterance.lower().find('hello') >= 0:  # default greeting response
                response = "".join(['Hello, ', mention, '!'])
                responding = True
            elif responding:  # all other responses
                if utterance.lower().find('Goodbye') >= 0:
                    response = "".join(['Bye bye, ', mention, '!'])
                    responding = False
                else:  # TODO generalize so that main() and discord can use ai
                    add_to_history(message.guild.id, message.author.id, utterance, message.created_at)
                    history = get_dialogue_history(message.guild.id, message.author.id)
                    intent = understand(utterance, history)
                    response = "".join([mention, " ", generate(intent[0], intent[1])])

            # send the response
            if response != '':
                await message.channel.send(response)


            # check message
            global msg
            msg = message


## Set up and log in
client = MyClient()
bot_token = get_discord_token()
responding = False
client.run(bot_token)
