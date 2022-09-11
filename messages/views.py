import re
from flask import request
from slack_bolt import Say

from . import messages_bp
from extensions import database, slack_manager

client = slack_manager.get_client()
bolt_app = slack_manager.get_bolt_app()
handler = slack_manager.get_handler()


@bolt_app.message("hello slacky")
def greetings(payload: dict, say: Say):
    """ This will check all the message and pass only those which has 'hello slacky' in it """
    user: str = payload.get("user")
    say(f"Hi <@{user}>")


@bolt_app.message(re.compile("(hi|hello|hey) slacky", re.IGNORECASE))
def reply_in_thread(payload: dict):
    """ This will reply in thread instead of creating a new thread """
    response = client.chat_postMessage(channel=payload.get('channel'),
                                       thread_ts=payload.get('ts'),
                                       text=f"Hi <@{payload['user']}> in <@{payload['channel']}>")

@messages_bp.route("/channel-response-bot/events", methods=["POST"])
def slack_events():
    """ Declaring the route where slack will post a request """
    return handler.handle(request)