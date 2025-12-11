import IoManager

class LexiconManager:
    _instance = None

    # Makes this a singleton
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LexiconManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.lexicons = []
        self.indexes = {}


    def get_lexicon(self, name):
        if name in self.indexes:
            return self.lexicons[self.indexes[name]]
        else:
            try:
                word_list = IoManager.load_lexicon(name)
                self.indexes[name] = len(self.lexicons)
                self.lexicons.append(word_list)
                return word_list

            except:
                pass

    def clear_lexicons(self):
        self.lexicons = []
        self.indexes = {}
