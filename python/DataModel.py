from PySide6.QtCore import QObject, Property, Signal, Slot, QAbstractListModel

class RulesModel(QAbstractListModel):
    ruleListChanged = Signal()

    def __init__(self):
        super().__init__()
        self._rule_list = ["Apple", "Banana", "Cherry"]

    @Property("QStringList", notify=ruleListChanged)
    def rule_list(self):
        return self._rule_list

    @Slot()
    def update_list(self, rules):
        self._rule_list = rules
        self.ruleListChanged.emit()
