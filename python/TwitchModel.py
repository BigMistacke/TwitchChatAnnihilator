from PySide6.QtCore import QObject, Property, Signal, Slot, QAbstractListModel

class TwitchModel(QAbstractListModel):
    channelChanged = Signal()
    userChanged = Signal()
    loginChanged = Signal()
    runningChanged = Signal()


    def __init__(self):
        super().__init__()
        self._current_channel = ""
        self._current_user = ""
        self._logged_in = False
        self._running = False


    @Property("QString", notify=channelChanged)
    def current_channel(self):
        return self._current_channel

    @Slot()
    def update_channel(self, channel):
        self._current_channel = channel
        self.channelChanged.emit()


    @Property("QString", notify=userChanged)
    def current_user(self):
        return self._current_user

    @Slot()
    def update_user(self, user):
        self._current_user = user
        self.userChanged.emit()


    @Property(bool, notify=loginChanged)
    def current_login(self):
        return self._logged_in

    @Slot()
    def update_login(self, is_logged_in):
        self._logged_in = is_logged_in
        self.loginChanged.emit()


    @Property(bool, notify=runningChanged)
    def is_running(self):
        return self._running

    @Slot()
    def update_is_running(self, is_running):
        self._running = is_running
        self.runningChanged.emit()
