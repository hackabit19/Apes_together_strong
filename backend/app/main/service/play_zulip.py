import pprint
import zulip
import sys
import re
import httplib2
import os
from googletrans import Translator
from book_service import narrate_book

BOT_MAIL = "bhat-bot@zulipchat.com"

class ZulipBot(object):
    def __init__(self):
        self.client = zulip.Client(site="https://apes-together-strong.zulipchat.com/api/")
        self.subscribe_all()
        # self.hacknews = Hackernews()
        # self.trans = Translate()
        # self.movie = Movie()
        # self.lyrics = Lyrics()
        # self.holiday = Holiday()
        # self.currency = Currency()
        # self.cricket = Cricket()
        print("done init")
        self.subkeys = ["translate", "hackernews", "hn", "hotel", "HN", "askme", "cricnews", "movie", "currency", "holiday"]
    def subscribe_all(self):
        json = self.client.get_streams()["streams"]
        streams = [{"name": stream["name"]} for stream in json]
        self.client.add_subscriptions(streams)
    def process(self, msg):
        content = msg["content"].split()
        sender_email = msg["sender_email"]
        ttype = msg["type"]
        stream_name = msg['display_recipient']
        stream_topic = msg['subject']
        if sender_email == BOT_MAIL:
            return
        print("Successful heards.")
        if content[0].lower() == "bhatbot" or content[0] == "@**bhatbot**":
            if len(content) != 3:
                message = "Sorry! I don't understand."
                self.client.send_message({
                    "type": "stream",
                    "subject": msg["subject"],
                    "to": msg["display_recipient"],
                    "content": message
                })
            elif content[1].lower() in ["narrate_book", "narrate_note", "create_signs"]:
                command_type = content[1].lower()

                if command_type == "narrate_book":
                    audio_path = narrate_book(content[2], sound=True)
                    print("Don't worry, I will take forever to upload this file.")
                    with open(audio_path, 'rb') as fp:
                        result = self.client.call_endpoint(
                            'user_uploads',
                            method='POST',
                            files=[fp]
                        )
                    bot_handler.
                    message = "https://apes-together-strong.zulipchat.com" + result["uri"]

                    self.client.send_message({
                        "type": "stream",
                        "subject": msg["subject"],
                        "to": msg["display_recipient"],
                        "content": message
                    })

                # message = self.trans.translate(command_type, ip)

                # self.client.send_message({
                #     "type": "stream",
                #     "subject": msg["subject"],
                #     "to": msg["display_recipient"],
                #     "content": message
                # })

def main():
    bot = ZulipBot()
    bot.client.call_on_each_message(bot.process)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Thanks for interrupting me")
        sys.exit(0)

