

class TwitchMessage:
    def __init__(self, message_json):
        event = message_json.get("event", {})
        message = event.get("message", {})

        self.body = message.get("text", {})

        self.username = event.get("chatter_user_name", {})
        self.reply = event.get("reply", {})
        self.point_reward = event.get("channel_points_custom_reward_id", {})
        self.created = message_json.get("subscription", {}).get("created_at", {})

        self.roles = []
        for role in message.get("badges", {}):
            self.roles.append(role.get("set_id", {}))


        self.emotes = 0
        self.bits = 0
        self.mentions = []
        for fragment in message.get("fragments", {}):
            if fragment.get("type", {}) == "emote":
                if fragment.get("cheermote", {})  != {}:
                    self.bits += fragment.get("cheermote", {}).get("bits")

                if fragment.get("emote", {}) != {}:
                    self.emotes += 1

                if fragment.get("mention", {})  != {}:
                    self.mentions.append(fragment.get("mention", {})).get("user_name")


        # Cheeky backup code in case the above for-loop doesn't work
        # for fragment in message.get("fragments", []):
        #     ftype = fragment.get("type")

        #     # Count emotes
        #     if ftype == "emote":
        #         if fragment.get("emote") is not None:
        #             self.emotes += 1

        #     # Count bits / cheermotes
        #     if ftype == "cheermote":
        #         cheermote = fragment.get("cheermote")
        #         if cheermote and "bits" in cheermote:
        #             self.bits += cheermote["bits"]

        #     # Collect mentions
        #     if ftype == "mention":
        #         mention = fragment.get("mention")
        #         if mention and "user_name" in mention:
        #             self.mentions.append(mention["user_name"])


    def __init__(self, body = "", username = "", reply = False, point_reward = "", created = "", roles = [], emotes = 0, cheer = 0, mentions = 0):
        self.body = body
        self.username = username
        self.reply = reply
        self.point_reward = point_reward
        self.created = created
        self.roles = roles
        self.emotes = emotes
        self.cheer = cheer
        self.mentions = mentions
