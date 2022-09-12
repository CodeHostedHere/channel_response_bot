from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import os

class SlackManager:
    def __init__(self):
        self.client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
        self.bolt_app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))
        self.handler = SlackRequestHandler(self.bolt_app)
    
    def get_client(self):
        return self.client

    def get_bolt_app(self):
        return self.bolt_app

    def get_handler(self):
        return self.handler