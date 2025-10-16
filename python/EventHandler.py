from PySide6.QtCore import QObject, Slot

import IoManager

class EventHandler(QObject):
    def __init__(self, twitch_manager):
        super().__init__()

        self._twitch_manager = twitch_manager

    @Slot()
    def toggle_ban_bot(self):
        if(self._twitch_manager.ban_bot_active):
            self._twitch_manager.stop_ban_bot()
        else:
            self._twitch_manager.start_ban_bot()


    @Slot(result=str)
    def login(self):
        return self._twitch_manager.login()

    @Slot(str)
    def set_channel(self, channel):
        self._twitch_manager.set_channel(channel)


    @Slot(result=str)
    def get_rule_list():
        return IoManager.get_rule_list()
