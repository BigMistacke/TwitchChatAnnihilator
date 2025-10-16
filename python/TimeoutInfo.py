from PySide6.QtCore import QObject, Signal, Slot

class TimeoutInfo(QObject):
    timeoutInfoUpdated = Signal(str, str, str, int, bool)

    def __init__(self):
        super().__init__()

    @Slot()
    def update_data(self, new_user, new_message, new_reason, new_duration, new_acceptable):
        username = new_user
        message = new_message
        reason = new_reason
        duration = new_duration
        acceptable = new_acceptable
        self.timeoutInfoUpdated.emit(username, message, reason, duration, acceptable)
