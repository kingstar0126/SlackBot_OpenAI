########################################################################################################################
############# ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ SLACKBOT APP INTEGRATION ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #############
########################################################################################################################

import os
import random
import time

from slack_sdk import WebClient
from response_map import response_dict
from triggers import get_response_key


# Bot settings & connection handlers
BOT_NAME = "Niki"
BOT_ID = "@U02T8E6QBPG"

WEB_CLIENT = WebClient(token=os.environ.get("SLACKBOT_NIKI_TOKEN"))

CHANNEL_NAME = "few-new-innovations"
CONVERSATION_ID = None


def handle_command(command): #, channel):
    """Take cleaned command, look up response, and post to channel"""

    # Check for exact matches first then check for contained keywords
    print(f" {BOT_NAME}: Command: {command}")
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

        print(f" {BOT_NAME}: now online!")
        print(f" {BOT_NAME}: Serving channel: {CHANNEL_NAME}, Conversation ID: {CONVERSATION_ID}")

        while CONVERSATION_ID:
            try:
                result = WEB_CLIENT.conversations_history(
                        channel=CONVERSATION_ID, inclusive=False,
                        oldest=str(int(time.time())-1), limit=1)

                text = result["messages"][0]["text"] if result["messages"] else None

                if text and BOT_ID in text:
                    command = text.split(BOT_ID)[1].strip('>').lstrip().lower()

                    if command:
                        handle_command(command)

                time.sleep(1)  # websocket read delay

            except Exception as e:
                print(f" {BOT_NAME}: Error: {e}")
        else:
            print(f" {BOT_NAME}: No Conversation ID found. Please check channel name for validity.")

    except Exception as e:
        print(f" {BOT_NAME}: Error: {e}")
