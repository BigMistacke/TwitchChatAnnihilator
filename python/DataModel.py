from PySide6.QtCore import QObject, Property, Signal, Slot, QAbstractListModel

class DataModel(QAbstractListModel):
    ruleListChanged = Signal()
    currentRuleChanged = Signal()
    ruleIndexChanged = Signal()

    lexiconListChanged = Signal()
    currentLexiconChanged = Signal()
    lexiconIndexChanged = Signal()


    def __init__(self):
        super().__init__()
        self._rule_list = [""]
        self._current_rule = ""
        self._current_rule_index = 0

        self._lexicon_list = [""]
        self._current_lexicon = ""
        self._current_lexicon_index = 0


    @Property("QStringList", notify=ruleListChanged)
    def rule_list(self):
        return self._rule_list

    @Slot()
    def update_rule_list(self, rules):
        self._rule_list = rules
        self.ruleListChanged.emit()

    @Property("QString", notify=currentRuleChanged)
    def current_rule(self):
        return self._current_rule

    @Slot()
    def update_current_rule(self, rule):
        self._current_rule = rule
        self.currentRuleChanged.emit()

    @Property("QString", notify=currentRuleChanged)
    def current_rule_name(self):
        return self._rule_list[self._current_rule_index]


    @Property("int", notify=ruleIndexChanged)
    def current_rule_index(self):
        return self._current_rule_index

    @Slot()
    def update_rule_index(self, index):
        self._current_rule_index = index
        self.ruleIndexChanged.emit()



    @Property("QStringList", notify=lexiconListChanged)
    def lexicon_list(self):
        return self._lexicon_list

    @Slot()
    def update_lexicon_list(self, lexicons):
        self._lexicon_list = lexicons
        self.lexiconListChanged.emit()

    @Property("QString", notify=currentLexiconChanged)
    def current_lexicon(self):
        return self._current_lexicon

    @Slot()
    def update_current_lexicon(self, lexicon):
        self._current_lexicon = str(lexicon)
        self.currentLexiconChanged.emit()

    @Property("QString", notify=currentLexiconChanged)
    def current_lexicon_name(self):
        return self._lexicon_list[self._current_lexicon_index]

    @Property("int", notify=lexiconIndexChanged)
    def current_lexicon_index(self):
        return self._current_lexicon_index

    @Slot()
    def update_lexicon_index(self, index):
        self._current_lexicon_index = index
        self.lexiconIndexChanged.emit()
