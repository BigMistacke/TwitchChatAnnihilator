import threading
import requests
import time
import json

from BanBot import BanBot
import secrets #This stores stuff I don't want in the commits like the client id.  The only thing in it are a few hard coded variables
import IoManager


class TwitchManager():
    def __init__(self, filter, timeout_info, twitch_model):
        self._client_id = secrets.client_id
        self._scope = "moderator:manage:banned_users user:write:chat user:read:chat"

        self._ban_bot = BanBot(filter, timeout_info)
        self._twitch_model = twitch_model

        self.stop_event = threading.Event()
        self._refresh_thread = threading.Thread(target=self._renew_tokens_loop)

        self._access_token = ""
        self._refresh_token = ""
        self._expiry = 0

        tokens = IoManager.load_tokens()
        if "refresh_token" in tokens:
            self._refresh_token = tokens["refresh_token"]

            if not self._access_token == "":
                self._get_user_id()
                self.start_token_check()

        settings = IoManager.load_settings()
        if "channel" in settings:
            self.set_channel(setting["channel"])




    def login(self):
        response = requests.post(
            "https://id.twitch.tv/oauth2/device",
            data={
                "client_id": self._client_id,
                "scopes": self._scope
            }
        )
        if response.status_code == 200:
            response_json = response.json()

            token_thread = threading.Thread(target=self._get_new_tokens, args=( response_json["device_code"], response_json["expires_in"], response_json["interval"]), daemon=True)
            token_thread.start()

            return response_json["verification_uri"], response_json["user_code"]


    def _get_new_tokens(self, device_code, expires_in=1800, interval=5):
        expires_on = time.time() + expires_in

        while True:
            if time.time() > expires_on:
                print("Device code expired.")
                break

            response = requests.post(
                "https://id.twitch.tv/oauth2/token",
                data={
                    "client_id": self._client_id,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                }
            )
            response_data = response.json()

            if response.status_code == 200:
                self._access_token = response_data["access_token"]
                self._ban_bot.set_token(self._access_token)
                self._refresh_token = response_data["refresh_token"]
                self._expiry = response_data["expires_in"] + time.time()

                self._twitch_model.update_login(True)
                self._get_user_id()
                self.start_token_check()

                tokens = {
                    "refresh_token": self._refresh_token
                }
                IoManager.save_tokens(tokens)
                break

            elif response.status_code == 400:

                if response_data["message"] == "authorization_pending":
                    pass
                elif response_data["message"] == "slow_down":
                    interval += 5

                elif response_data["message"] == "expired_token":
                    print("Device code has expired.")
                    break
                else:
                    print("Unexpected error: {error}")
                    break

            else:
                print(f"Unexpected status code: {response.status_code}")
                print(response.text)
                break

            time.sleep(interval)

    def logout():
        self.stop_event.set()
        self._twitch_model.update_login(False)
        self.start_ban_bot()
        self._access_token = ""
        self._refresh_token = ""
        self._expiry = 0
        self._ban_bot.set_token("")
        self._ban_bot.set_user_id("")
        IoManager.save_tokens({
            "refresh_token": "self._refresh_token"
        })

    def _renew_tokens(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token,
            'client_id': self._client_id
        }

        response = requests.post("https://id.twitch.tv/oauth2/token", headers=headers, data=data)
        data = response.json()

        if response.status_code == 200:
            self._access_token = data["access_token"]
            self._ban_bot.set_token(self._access_token)
            self._refresh_token = data["refresh_token"]
            self._expiry = data["expires_in"] + time.time()
            self._twitch_model.update_login(True)


            tokens = {
                "refresh_token": self._refresh_token
            }
            IoManager.save_tokens(tokens)

        #I'm not sure if I need to specifically join the threads in order to avoid a memory leak
        elif response.status_code == 400:
            if data["message"] == "missing refresh token":
                self.logout()
            if data["message"] == "Invalid refresh token":
                self.logout()
            else:
                print("Unexpected error: {error}")


    def _renew_tokens_loop(self):
        while(not self.stop_event.is_set()):
            if time.time() > self._expiry-60:
                self._renew_tokens
            time.sleep(60)


    def start_token_check(self):
        self._refresh_thread = threading.Thread(target=self._renew_tokens_loop)
        self.stop_event.clear()
        self._refresh_thread.start()

    def kill_manager(self):
        self.stop_ban_bot()
        self.stop_event.set()


    #Catch 'invalid token' error, try to refresh token, otherwise 'logout'
    def start_ban_bot(self):
        self._twitch_model.update_running(True)
        self._ban_bot.start()

    def stop_ban_bot(self):
        self._twitch_model.update_running(False)
        self._ban_bot.stop()


    def set_filter(self, filter):
        self._ban_bot.set_filter(filter)

    def set_channel(self, channel):
        self._twitch_model.update_channel(channel)
        headers = {
            "Authorization": "Bearer " + self._access_token,
            "Client-Id": self._client_id,
            "Content-Type": "application/json"
        }

        response = requests.get(f"https://api.twitch.tv/helix/users?login={channel}", headers=headers)
        data = response.json()

        if data["data"] != [] and data["data"][0]["id"]:
            try:
                self._ban_bot.set_channel(data["data"][0]["id"])
                self._twitch_model.update_channel(channel)
            except:
                pass
                #Should set up a proper error here



    def _get_user_id(self):
        headers = {
            'Authorization': 'OAuth ' + self._access_token,
            'client_id': self._client_id
        }

        response = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers)
        data = response.json()
        self._ban_bot.set_user_id(data["user_id"])
        self._twitch_model.update_user(data["login"])

