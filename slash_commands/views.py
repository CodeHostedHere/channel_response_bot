import re
from flask import request

from . import slash_cmds_bp
from extensions import database
from extensions import slack_manager

client = slack_manager.get_client()
bolt_app = slack_manager.get_bolt_app()
handler = slack_manager.get_handler()



@slash_cmds_bp.route("/channel-response-bot/commands", methods=["POST"])
def slack_commands():
    """Declaring the route for command management"""
    return handler.handle(request)

def split_command_by_type(command_received):
    """ Split in to regex or simple message cue """
    response_to_automate, command_without_response = "", ""
    try:
        response_to_automate, command_without_response = re.split("Cue:", command_received, flags=re.IGNORECASE)
        print(f"1: response_to_automate {response_to_automate} command_without_response {command_without_response}")
    except: 
        try:
            response_to_automate, command_without_response = re.split("Regex:", command_received, flags=re.IGNORECASE)
            print(f"2: response_to_automate {response_to_automate} command_without_response {command_without_response}")

        except:
            print("First exception")
            raise Exception("Command does not contain 'Cue:' or 'Regex:'")
    print(f"3: response_to_automate {response_to_automate} command_without_response {command_without_response}")
    return response_to_automate.strip("\"\', "), command_without_response.strip("\"\', ")

def parse_trigger_and_channel(command_without_response, payload):
    """ Split message received based on the string in:. 
    Return trigger and channel id """

    print(f"cmd_wo_resp {command_without_response}")
    trigger_phrase, channel_name_and_id, channel_id = "", "", ""
    try:
        trigger_phrase, channel_name_and_id = re.split("In:", command_without_response, flags=re.IGNORECASE)
        trigger_phrase = trigger_phrase.strip("\"\', ")
        channel_name_and_id = channel_name_and_id.strip("\"\', ")
    except:
        trigger_phrase = command_without_response
        channel_id = payload['channel_id']
        print("Does not contain In:, default to current channel")
        return trigger_phrase, channel_id

    # Slack puts in the channel name and ID separated by a |, if the channel can be found
    try:
        channel_id = channel_name_and_id.split("|")[0].strip("<#")
    except:
        raise Exception("Channel name given is incorrect, please check the spelling and try again")
        
    return trigger_phrase, channel_id
    
@bolt_app.command("/add-response")
def help_command(payload, say, ack):
    """ This is for slash command /add-response """
    # /add-response Response:"My Response", Cue:"Someone's Message", In:"#Channel" or
    # /add-response Response:"My Response", Regex:"Someone's Message", In:"#Channel"
    ack()
    print("Started")
    response_to_automate, trigger_phrase, channel_id, response_for_client = "", "", "", ""
    print(payload)
    try:
        if "text" not in payload:
            raise Exception("No message received after command")
        command_received = payload['text']
        print(f"command_received {command_received}")
        response_to_automate, command_without_response = split_command_by_type(command_received)
        trigger_phrase, channel_id = parse_trigger_and_channel(command_without_response, payload)
    except Exception as e:
        response_for_client = str(e)
        print(response_for_client)
        say(response_for_client)
        return
    response_for_client = f"Response to automate: {response_to_automate}, trigger_phrase: {trigger_phrase}, channel_id: {channel_id}, team_id: {payload['team_id']}, team_domain: {payload['team_domain']}"
    say(response_for_client)





