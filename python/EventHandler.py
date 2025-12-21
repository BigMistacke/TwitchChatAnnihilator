from PySide6.QtCore import QObject, Slot

from TwitchMessage import TwitchMessage
import IoManager
import Filter


class EventHandler(QObject):
    def __init__(self, twitch_manager, data_model, twitch_model):
        super().__init__()

        self._twitch_manager = twitch_manager
        self.data_model = data_model

        rule_list = IoManager.retrieve_rule_list()
        self.data_model.update_rule_list(rule_list)
        self.select_rule(0)

        lexicon_list = IoManager.get_lexicon_list()
        self.data_model.update_lexicon_list(lexicon_list)
        self.select_lexicon(0)

    def create_filter(self):
        rule_list = IoManager.retrieve_rule_list()
        index = self.data_model.current_rule_index
        current_rule = IoManager.retrieve_rule(rule_list[index])

        filter = Filter.create_filter(current_rule)
        self._twitch_manager.set_filter(filter)

    def update_rule_list(self):
        rule_list = IoManager.retrieve_rule_list()
        self.data_model.update_rule_list(rule_list)

    def update_lexicon_list(self):
        lexicon_list = IoManager.get_lexicon_list()
        self.data_model.update_lexicon_list(lexicon_list)



    @Slot()
    def start_ban_bot(self):
        self.create_filter()
        self._twitch_manager.start_ban_bot()

    @Slot()
    def stop_ban_bot(self):
        self._twitch_manager.stop_ban_bot()


    @Slot(result='QVariantMap')
    def login(self):
        url, code = self._twitch_manager.login()
        return {"url": url, "code": code}

    @Slot()
    def logout(self):
        return self._twitch_manager.logout()

    @Slot(str)
    def set_channel(self, channel):
        self._twitch_manager.set_channel(channel)




    @Slot(int)
    def select_rule(self, index):
        rule_list = IoManager.retrieve_rule_list()
        if(len(rule_list) != 0):
            current_rule = IoManager.retrieve_rule(rule_list[index])
        else:
            current_rule = ""
        self.data_model.update_current_rule(current_rule)
        self.data_model.update_rule_index(index)


    @Slot(str)
    def save_rule(self, new_rule):
        current_rule = self.data_model.current_rule_name
        IoManager.save_rule(current_rule, new_rule)
        self.data_model.update_current_rule(new_rule)

    @Slot(str, str)
    def save_rule_as(self, new_rule, new_name):
        current_rule = self.data_model.current_rule_name
        IoManager.delete_rule(current_rule)
        IoManager.save_rule(new_name, new_rule)
        self.update_rule_list()


    @Slot()
    def delete_rule(self):
        current_rule = self.data_model.current_rule_name
        IoManager.delete_rule(current_rule)
        self.update_rule_list()
        self.select_rule(0)


    @Slot(result=str)
    def new_rule(self):
        new_rule = IoManager.new_rule()
        self.update_rule_list()
        rule_list = IoManager.retrieve_rule_list()
        index = rule_list.index(new_rule)
        self.select_rule(rule_list.index(new_rule))


    @Slot(str, str, result='QVariantMap')
    def test_rule(self, rule, message):
        filter = Filter.create_filter(rule)
        twitch_message = TwitchMessage(message, "user")
        results = filter.test(twitch_message, 1000)
        print(results)
        return results



    @Slot(int)
    def select_lexicon(self, index):
        lexicon_list = IoManager.get_lexicon_list()
        if(len(lexicon_list) != 0):
            current_lexicon = IoManager.load_lexicon(lexicon_list[index], False)
        else:
            current_lexicon = ""

        self.data_model.update_current_lexicon(current_lexicon)
        self.data_model.update_lexicon_index(index)


    @Slot(str)
    def save_lexicon(self, new_lexicon):
        current_lexicon = self.data_model.current_lexicon_name
        IoManager.save_lexicon(current_lexicon, new_lexicon)
        self.data_model.update_current_lexicon(new_lexicon)


    @Slot(str, str)
    def save_lexicon_as(self, new_lexicon, new_name):
        current_lexicon = self.data_model.current_lexicon_name
        IoManager.delete_lexicon(current_lexicon)
        IoManager.save_lexicon(new_name, new_lexicon)
        self.update_lexicon_list()


    @Slot()
    def delete_lexicon(self):
        current_lexicon = self.data_model.current_lexicon_name
        IoManager.delete_lexicon(current_lexicon)
        self.update_lexicon_list()
        self.select_lexicon(0)


    @Slot(result=str)
    def new_lexicon(self):
        new_lexicon = IoManager.new_lexicon()
        self.update_lexicon_list()
        lexicon_list = IoManager.get_lexicon_list()
        index = lexicon_list.index(new_lexicon)
        self.select_lexicon(lexicon_list.index(new_lexicon))


    @Slot(str)
    def import_lexicon(self, location):
        new_lex = IoManager.import_lexicon(location[7:])

        last_index = location.rfind('/')
        name = location[last_index + 1:-4]
        IoManager.save_lexicon(name, new_lex)

        self.update_lexicon_list()
        lexicon_list = IoManager.get_lexicon_list()
        index = lexicon_list.index(name)
        self.select_lexicon(lexicon_list.index(name))
