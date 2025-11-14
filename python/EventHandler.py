from PySide6.QtCore import QObject, Slot

from TwitchMessage import TwitchMessage
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

    def create_filter(self):
        rule_list = IoManager.retrieve_rule_list()
        index = self.data_model.current_index
        current_rule = IoManager.retrieve_rule(rule_list[index])

        filter = Filter.create_filter(current_rule)
        self._twitch_manager.set_filter(filter)

    def update_list(self):
        rule_list = IoManager.retrieve_rule_list()
        self.data_model.update_list(rule_list)


    @Slot()
    def toggle_ban_bot(self):
        if(self._twitch_manager.ban_bot_active):
            self._twitch_manager.stop_ban_bot()
        else:
            self.create_filter()
            self._twitch_manager.start_ban_bot()


    @Slot(result=str)
    def login(self):
        return self._twitch_manager.login()

    @Slot(str)
    def set_channel(self, channel):
        self._twitch_manager.set_channel(channel)




    @Slot(int)
    def select_rule(self, index):
        rule_list = IoManager.retrieve_rule_list()
        current_rule = IoManager.retrieve_rule(rule_list[index])

        self.data_model.update_current(current_rule)
        self.data_model.update_index(index)


    @Slot(str)
    def save_rule(self, new_rule):
        current_rule = self.data_model.current_rule_name()
        IoManager.save_rule(current_rule, new_rule)


    @Slot(str, str)
    def rename_rule(self, new_rule, new_name):
        current_rule = self.data_model.current_rule_name()
        IoManager.delete_rule(current_rule)
        IoManager.save_rule(new_name, new_rule)
        self.update_list()


    @Slot()
    def delete_rule(self):
        current_rule = self.data_model.current_rule_name()
        IoManager.delete_rule(current_rule)
        self.update_list()
        self.select_rule(0)


    @Slot(result=str)
    def new_rule(self):
        new_rule = IoManager.new_rule()
        self.update_list()
        rule_list = IoManager.retrieve_rule_list()
        index = rule_list.index(new_rule)
        self.select_rule(rule_list.index(new_rule))


    @Slot(str, str, result='QVariantMap')
    def test_rule(self, rule, message):
        filter = Filter.create_filter(rule)
        twitch_message = TwitchMessage(message, "user")
        results = filter.test(twitch_message, 1000)
        return results
