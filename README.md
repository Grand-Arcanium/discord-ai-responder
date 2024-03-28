# Discord AI Responder
This is a  framework for a Chat GPT-based responder for Discord Bots (Python).

This project is made by two students originally as an assignment for Intro to Intelligent Systems, as well as 
to practice Git and collaborative coding.

The `master/main` branch will be expanded from the assignment version into a proper framework in the future, 
while the `relevance-call` branch contains the finalized assignment **as is**.

## Setup
1) Download the required libraries found in `requirements.txt`
2) Store API keys into the following files:
- Discord: `discord_token.txt` (Make sure your app has, at minimum, basic read/write perms)
- OpenAPI: `gpt_token.txt`
- If you have different file names, change them to our recommended file names, 
or change their path in `config.py` to match. Then update `.gitignore` to match if you wish to push into git later.

3) There is a `prompts.json` already set up, containing the prompts and training for both calls. 
Feel free to edit as needed, as long as it follows the current format. This data is fed to the application 
itself, and **not** directly to the openAPI as fine-tuning data.
4) Run `discord_main.py` to start the bot, or run `responder.py` to start the app independently in
the console.