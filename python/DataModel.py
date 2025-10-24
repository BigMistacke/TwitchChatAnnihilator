from PySide6.QtCore import QObject, Property, Signal, Slot, QAbstractListModel

class DataModel(QAbstractListModel):
    ruleListChanged = Signal()
    currentRuleChanged= Signal()
    currentIndex= Signal()


    def __init__(self):
        super().__init__()
        self._rule_list = [""]
        self._current_rule = ""
        self._current_index = 0


    @Property("QStringList", notify=ruleListChanged)
    def rule_list(self):
        return self._rule_list

    @Slot()
    def update_list(self, rules):
        self._rule_list = rules
        self.ruleListChanged.emit()

    @Property("QString", notify=currentRuleChanged)
    def current_rule(self):
        return self._current_rule

    @Slot()
    def update_current(self, rule):
        self._current_rule = rule
        self.currentRuleChanged.emit()

    def current_rule_name(self):
        return self._rule_list[self._current_index]


    @Property("int", notify=currentIndex)
    def current_index(self):
        return self._current_index

    @Slot()
    def update_index(self, index):
        self._current_index = index
        self.currentIndex.emit()
