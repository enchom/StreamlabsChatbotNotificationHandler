#---------------------------
#   Import Libraries
#---------------------------

import clr
clr.AddReference("IronPython.Modules.dll")
clr.AddReference("websocket-sharp.dll")

import time
import os
import sys
import json
import WebSocketSharp

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Twitch Notifications"
Website = None
Description = "Please provide API Keys (Right click -> Insert API Key)"
Creator = "Enchom"
Version = "1.0.1.11"

#---------------------------
#   Notification logic
#---------------------------
global NotificationHandler
NotificationHandler = None
global ws
ws = None
global API_Info
API_Info = None


def log(s):
    Parent.Log(ScriptName, str(s))
    
def OnOpen(ws, e):
    auth = {}
    auth['author'] = 'Enchom'
    auth['website'] = None
    auth['api_key'] = API_Info['API_Key']
    auth['events'] = ['EVENT_SUB', 'EVENT_DONATION', 'EVENT_CHEER', 'EVENT_FOLLOW', 'EVENT_HOST']
    ws.Send(json.dumps(auth))
    
def OnClose(ws, e):
    pass
    
def OnMessage(ws, e):
    parsed_json = json.loads(e.Data)
    event = parsed_json['event']
    data = parsed_json['data']
    if isinstance(data, str):
        data = json.loads(data)
        
    if event == 'EVENT_SUB':
        NotificationHandler.on_subscription(data)
    elif event == 'EVENT_DONATION':
        NotificationHandler.on_donation(data)
    elif event == 'EVENT_CHEER':
        NotificationHandler.on_cheer(data)
    elif event == 'EVENT_FOLLOW':
        NotificationHandler.on_follow(data)
    elif event == 'EVENT_HOST':
        NotificationHandler.on_host(data)
        

def OnError(ws, e):
    log(e.Message)
    log(e.Exception)
    
def start_websocket():
    global ws
    if ws == None:
        ws = WebSocketSharp.WebSocket(API_Info['API_Socket'])
        ws.OnOpen += OnOpen
        ws.OnClose += OnClose
        ws.OnMessage += OnMessage
        ws.OnError += OnError
        ws.Connect()
    
def stop_websocket():
    global ws
    if ws != None:
        ws.Close()
        ws = None

def parse_api_data(fname):
    result = {}
    with open(fname, 'r') as file:
        data = file.read()
    declarations = list(filter(lambda x: '=' in x, data.split('var')))
    declarations = list(map(lambda x: x.strip(), declarations))
    declarations = list(map(lambda x: x[:-1] if x[-1] == ';' else x, declarations))
    for dec in declarations:
        split = list(map(lambda x: x.strip(), dec.split('=')))
        result[split[0]] = (split[1][1:-1] if split[1][0] == '"' or split[1][0] == "'" else split[1]).strip()
    
    return result

#---------------------------
#   Notification Handling
#---------------------------

class TwitchNotificationHandler(object):
    def __init__(self):
        pass
        
    def on_subscription(self, data):
        """
        Available values in 'data' are:
        name, display_name, tier, is_resub, months, message, gift_target
        """
        Parent.SendStreamMessage('Subscription for ' + str(data['months']) + ' from ' + str(data['display_name']))
        
    def on_follow(self, data):
        """
        Available values in 'data' are:
        name, display_name
        """
        Parent.SendStreamMessage('Follow from ' + data['display_name'])
        
    def on_donation(self, data):
        """
        Available values in 'data' are:
        userId, name, display_name, amount, currency, message
        """
        Parent.SendStreamMessage('Donation ' + str(data['amount']) + str(data['currency']))
        
    def on_cheer(self, data):
        """
        Available values in 'data' are:
        name, display_name, bits, total_bits, message
        """
        Parent.SendStreamMessage('Cheer ' + str(data['bits']) + ' bits')
        
    def on_host(self, data):
        """
        Available values in 'data' are:
        name, display_name, viewers
        """
        Parent.SendStreamMessage('Host with ' + str(data['viewers']) + ' viewers from ' + str(data['display_name']))

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    global NotificationHandler, API_Info
    API_Info = parse_api_data(os.path.join(os.path.dirname(__file__), 'API_Key.js'))
    NotificationHandler = TwitchNotificationHandler()
    start_websocket()

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    stop_websocket()
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    if state:
        start_websocket()
    else:
        stop_websocket()
        
    return