from PySide6.QtCore import QObject, Slot

import IoManager
import Filter


class EventHandler(QObject):
    def __init__(self, twitch_manager, data_model):
        super().__init__()

        self._twitch_manager = twitch_manager

        rule_list = IoManager.retrieve_rule_list()
        current_rule = IoManager.retrieve_rule(rule_list[0])

        self.data_model = data_model
        self.data_model.update_list(rule_list)
        self.data_model.update_current(current_rule)

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


    @Slot(int)
    def select_rule(self, index):
        rule_list = IoManager.retrieve_rule_list()
        current_rule = IoManager.retrieve_rule(rule_list[index])

        filters = Filter.create_filter(current_rule)
        self._twitch_manager.set_filters(filters)

        self.data_model.update_current(current_rule)
        self.data_model.update_index(index)


    @Slot(str)
    def save_rule(self, new_rule):
        current_rule = self.data_model.current_rule_name()
        IoManager.save_rule(current_rule, new_rule)

