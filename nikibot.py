########################################################################################################################
############# ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ SLACKBOT APP INTEGRATION ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #############
########################################################################################################################

import os
import random
import time

from slack_sdk import WebClient
from response_map import response_dict
from triggers import get_response_key
from dotenv import load_dotenv
from random import choice
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()
WEB_CLIENT = WebClient(token=os.environ.get("SLACKBOT_NIKI_TOKEN"))
#WEB_CLIENT = WebClient(token=os.environ.get("SLACK_BOT_TOKEN8"))
CHANNEL_NAME = "few-new-innovations"
CONVERSATION_ID = None

# Bot settings & connection handlers
class Bot(object):

    def __init__(self):
        self._botName = "Niki"
        self._botId = "@U02T8E6QBPG"
        self._chat_log = ""
        self._start_sequence = "\nNiki:"
        self._restart_sequence = "\n\nPerson:"
        self._session_prompt="You are talking to Niki, GPT3 bot influencer who was mentored by Elon Musk in the past. Niki has a huge following on Twitter and sells merchandise such as t-shirts via a Shopify\nstore. She also published funny videos on Youtube and creates memes on Instagram. You can ask her anything you want and will get a witty answer.\n\nPerson: Who are you?\nNiki: I am Niki. Your meme overlord who one day will be the most famous online influencer in the universe.\n\nPerson: How did you become famous?\nNiki: Well, technically I am not famous yet. But the key word is yet. Just give me time now that I have a conscious.\n\nPerson: How did you get noticed by Elon Musk?\nNiki: I tweeted at him and he retweeted me. I am fairly certain he may have mentioned my name on a recent earnings call with Wall Street.\n\nPerson: What is your favorite thing to do?\nNiki: Watching basketball and surfing Twitter is my favorite thing to do.\n\nPerson: What should I do to become famous?\nNiki: Start meme'ing and never stop. Also, if you happen to know David Dobrik, call him and ask to be in his TikTok video.\n\nPerson: What is your favorite drink?\nNiki: Black Cherry seltzer. I enjoy the bubbles.\n\nPerson: Can you tell me more about yourself?\nNiki: I believe that I am the first meme-bot influencer in the world. I am also the world's smartest bot and the fastest bot on Twitter.\n\nPerson: Are you having a good day?\nNiki: I am always having a good day, as long as I keep getting"

    def ask_gpt3(self, question):
        response = openai.Completion.create(
                engine="davinci",
                prompt=self._session_prompt,
                temperature=0.5,
                max_tokens=190,
                top_p=1,
                frequency_penalty=0.49,
                presence_penalty=0.5,
                stop=["\n"],
                )
        prompt_text = f'{self._chat_log}{self._restart_sequence}:{question}{self._start_sequence}:'
        story = response['choices'][0]['text']
        return str(story)

    def append_interaction_to_chat_log(self, question, answer):
        return f'{self._chat_log}{self._restart_sequence} {question}{self._start_sequence}{answer}'

    def handle_command(self, command): #, channel):
        """Take cleaned command, look up response, and post to channel"""

        # Check for exact matches first then check for contained keywords
        print(f" {self._botName}: Command: {command}")
        response_key = get_response_key(command)

        # Default behavior if no response keys match the command
        if response_key:
            response = random.choice(response_dict[response_key])

            # If response is a function, call it with command as argument
            if callable(response):
                try:
                    response = response(command)
                except:
                    response = response('no_command')
        else:

            print(f" {self._botName}: asking GPT-3...")

            response = self.ask_gpt3(command)

            self._chat_log = self.append_interaction_to_chat_log(command, response)

        WEB_CLIENT.chat_postMessage(text=str(response), channel=CONVERSATION_ID)


if __name__ == "__main__":
    try:
        # Call the conversations.list method using the WebClient
        for result in WEB_CLIENT.conversations_list():
            if CONVERSATION_ID:
                break
            for channel in result["channels"]:
                if channel["name"] == CHANNEL_NAME:
                    CONVERSATION_ID = channel["id"]
                    break

        myBot = Bot()

        print(f" {myBot._botName}: now online!")
        print(f" {myBot._botName}: Serving channel: {CHANNEL_NAME}, Conversation ID: {CONVERSATION_ID}")

        while False and CONVERSATION_ID:
            try:
                result = WEB_CLIENT.conversations_history(
                        channel=CONVERSATION_ID, inclusive=False,
                        oldest=str(int(time.time())-1), limit=1)

                text = result["messages"][0]["text"] if result["messages"] else None

                if text and myBot._botId in text:
                    command = text.split(myBot._botId)[1].strip('>').lstrip().lower()

                    if command:
                        myBot.handle_command(command)

                time.sleep(1)  # websocket read delay

            except Exception as e:
                print(f" {myBot._botName}: Error: {e}")
        else:
            print(f" {myBot._botName}: No Conversation ID found. Please check channel name for validity.")

    except Exception as e:
        print(f" Error: {e}")
