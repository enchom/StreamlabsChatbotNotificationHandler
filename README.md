# Streamlabs Chatbot Twitch Notifications
This is a very basic script that offers handling Twitch notifications such as donations, subs, cheers, etc, directly within a script. 

The project does not contain any UI, settings or overlay - for more information regarding those refer to 
https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate

The approach is the same as the one used in overlays in Chatbot scripts - a websocket is opened and listens for events.

## How to use
The project consists of a single file that can be directly imported as a script. The purpose of the project is to use it as a base, in particular the notification-handling functionality should be added in the class TwitchNotificationHandler.
