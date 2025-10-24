import threading
import websocket
import requests
import time
import json

import secrets
from TwitchMessage import TwitchMessage


class BanBot():
    def __init__(self, filters, timeout_info):
        self.access_token = ""
        self.client_id = secrets.client_id

        # self.username = ""
        self.user_id = ""
        self.channel = ""

        self.running = True

        self.filters = filters
        self.timeout_info = timeout_info

        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._create_session)


    def start(self):
        self.thread = threading.Thread(target=self._create_session)
        self.stop_event.clear()
        self.thread.start()


    #There is a chance this causes a memory leak. I'm not sure how good Python's garbage collection is.
    def stop(self):
        self.stop_event.set()


    def _create_session(self):
        ws = websocket.create_connection("wss://eventsub.wss.twitch.tv/ws")
        url = "https://api.twitch.tv/helix/eventsub/subscriptions"


        while(not self.stop_event.is_set()):
            print("Connected to Twitch WebSocket!")

            initial_message = ws.recv()
            initial_json = json.loads(initial_message)

            if initial_json.get("payload", {}).get("session", {}).get("status") != "connected":
                #Throw error
                return


            session_id = initial_json.get("payload", {}).get("session", {}).get("id")
            keep_alive_timer = initial_json.get("payload", {}).get("session", {}).get("keepalive_timeout_seconds")
            deadline = time.time() + keep_alive_timer

            headers = {
                "Authorization": "Bearer " + self.access_token,
                "Client-Id": secrets.client_id,
                "Content-Type": "application/json"
            }

            data = {
                "type": "channel.chat.message",
                "version": "1",
                "condition": {
                    "broadcaster_user_id": self.channel,
                    "user_id": self.user_id
                },
                "transport": {
                    "method": "websocket",
                    "session_id": session_id
                }
            }

            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 401:
                print(response)
                break

            while( not self.stop_event.is_set()):
            # while( not self.stop_event.is_set() and time.time() < deadline):
                message = ws.recv()
                message_json = json.loads(message)

                message_type = message_json.get("metadata", {}).get("message_type", {})

                if(message_type == "session_keepalive"):
                    deadline = time.time() + keep_alive_timer
                else:
                    twitch_message = self._format_message(message_json.get("payload", {}))
                    self._check_message(twitch_message)

                time.sleep(0.5)


    def _format_message(self, message):
        body = message.get("event", {}).get("message", {}).get("text", {})
        user = message.get("event", {}).get("chatter_user_name", {})

        twitch_message = TwitchMessage(body, user)
        return twitch_message


    def _check_message(self, message):
        result = ""
        for filter in self.filters:
            result = filter.evaluate(message)
            if(result[0] == True):
                break

        if (not self.stop_event.is_set()):
            self.timeout_info.update_data(message.user, message.body, result[2], result[1], result[0])
            self.ban_user(message.user, result[1], result[2])

    def ban_user(self, target, duration, message):
        url = f"https://api.twitch.tv/helix/moderation/bans?broadcaster_id={self.channel}&moderator_id={self.user_id}"

        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Client-Id": self.client_id,
            "Content-Type": "application/json"
        }

        data = {
            "data": {
                "user_id": target,
                "duration": duration,  # Use an integer here, or remove if permanent ban
                "reason": message
            }
        }

        response = requests.post(url, headers=headers, json=data)
        print("Response:", response.json())


    def set_token(self, token):
        self.access_token = token

    def set_user_id(self, id):
        self.user_id = id

    def set_channel(self, id):
        self.channel = id

    def set_filters(self, filters):
        self.filters = filters
