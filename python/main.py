from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl

import sys
import threading
import time

from TimeoutInfo import TimeoutInfo
from TwitchManager import TwitchManager
from EventHandler import EventHandler
from DataModel import DataModel
import IoManager

import Filter

from TwitchMessage import TwitchMessage

def main():
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()


    rule_list = IoManager.retrieve_rule_list()
    current_rule = IoManager.retrieve_rule(rule_list[0])
    filter = Filter.create_filter(current_rule)

    timeout_info = TimeoutInfo()
    twitch_manager = TwitchManager(filter, timeout_info)

    data_model = DataModel()
    event_handler = EventHandler(twitch_manager, data_model)

    engine.rootContext().setContextProperty("TimeoutInfo", timeout_info)
    engine.rootContext().setContextProperty("EventHandler", event_handler)
    engine.rootContext().setContextProperty("DataModel", data_model)


    engine.load(QUrl("qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
