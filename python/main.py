from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl

import sys
import threading
import time

from TimeoutInfo import TimeoutInfo
from TwitchManager import TwitchManager
from EventHandler import EventHandler
from RulesModel import RulesModel
import IoManager

import Filter


Rulez = '''
timeout 15 cooldown 0 reason "Has fifth glyph": [
    contains["e"]
]
'''


def main():
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    timeout_info = TimeoutInfo()

    rule_list = IoManager.retrieve_rule_list()
    rules_model = RulesModel()
    rules_model.update_list(rule_list)

    filters = Filter.create_filter(IoManager.retrieve_rule(rule_list[0]))
    twitch_manager = TwitchManager(filters, timeout_info)

    event_handler = EventHandler(twitch_manager)

    engine.rootContext().setContextProperty("TimeoutInfo", timeout_info)
    engine.rootContext().setContextProperty("EventHandler", event_handler)
    engine.rootContext().setContextProperty("RulesModel", rules_model)


    engine.load(QUrl("qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
