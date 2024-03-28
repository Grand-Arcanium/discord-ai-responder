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
from data_handler import *


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
        Called when the bot is fully logged in. Has an integrated function call used
        to format a JSON file this bot needs for data handling and storage.

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

        # Bot does not respond to itself or other bots
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
                # if statement to make bot stop responding
                if utterance.lower().find('goodbye') >= 0:
                    response = "".join(['Bye bye, ', mention, '!'])
                    responding = False
                else:
                    # We add this message to its pertinent location in the JSON data structure for future reference
                    add_to_history(message.guild.id, message.author.id, utterance, message.created_at)
                    # We get a snippet of the conversation history that this bot has, specific to the user and server
                    # from which the message originates
                    history = get_dialogue_history(message.guild.id, message.author.id)
                    # We feed the conversation history and message to the bot, so it can detect our intent and tone
                    intent = understand(utterance, history)
                    # We feed the intent, history, and message to the bot so it can generate an appropriate response
                    response = "".join([mention, " ", generate(intent, history, utterance)])

            # send the response, only if its not an empty string
            if response != '':
                await message.channel.send(response)


# Set up a client and log in
client = MyClient()
bot_token = get_discord_token()
responding = False
client.run(bot_token)
