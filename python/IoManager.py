import json
import os
import string


base_path = "./"


def load_tokens():
    file_path = base_path + 'tokens.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                # File is empty or invalid JSON
                return {}
    else:
        return {}

def save_tokens(tokens):
    file_path = base_path + 'tokens.json'
    with open(file_path, 'w') as file:
        json.dump(tokens, file)


def load_settings():
    file_path = base_path + 'settings.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                # File is empty or invalid JSON
                return {}
    else:
        return {}

def save_settings(settings):
    file_path = base_path + 'settings.json'
    with open(file_path, 'w') as file:
        json.dump(settings, file)

def retrieve_rule_list():
    file_path = base_path + 'rules'

    rule_list = []
    if os.path.exists(file_path):
        for f in os.scandir(file_path):
            if f.is_file() and f.name.endswith(".tca"):
                rule_list.append(f.name[:-4])
    else:
        os.mkdir(file_path)

    return sorted(rule_list)

def retrieve_rule(name):
    file_path = base_path + 'rules/'
    if os.path.exists(file_path + name + ".tca",):
        with open(file_path + name + ".tca", 'r') as file:
            return file.read()


def save_rule(name, rule):
    file_path = base_path + 'rules/'
    with open(file_path + name + ".tca", 'w') as file:
        return file.write(rule)

def delete_rule(name):
    file_path = base_path + 'rules/'
    if os.path.exists(file_path + name + ".tca"):
        os.remove(file_path + name + ".tca")


def new_rule():
    file_path = base_path + 'rules/'

    rule_name = "new_rule"
    counter = 1

    blank_rule = """timeout 15 cooldown 0 reason "new rule" -
    contains["words"]
"""

    if os.path.exists(file_path + rule_name + ".tca"):
        while os.path.exists("./rules/"+"new_rule"+str(counter)+".tca"):
            counter += 1

        rule_name = "new_rule" + str(counter)
        with open(file_path + rule_name + ".tca", 'w') as file:
            file.write(blank_rule)

    else:
        with open(file_path + rule_name + ".tca", 'w') as file:
            file.write(blank_rule)

    return rule_name


def load_messages_said():
    file_path = base_path + 'said_messages.txt'

    loaded_messages= []

    try:
        with open(file_path, 'r') as f:
            # Read all lines from the file
            lines = f.readlines()

            # Strip the newline character from each line
            loaded_messages = [line.strip() for line in lines]

        return(loaded_messages)

    except FileNotFoundError:
        return []

def save_messages_said(messages):
    file_path = base_path + 'said_messages.txt'
    with open(file_path, 'w') as f:
        for message in messages:
            f.write(word + '\n')

def load_words_said():
    file_path = base_path + 'said_words.txt'
    loaded_words = []

    try:
        with open(file_path, 'r') as f:
            # Read all lines from the file
            lines = f.readlines()

            # Strip the newline character from each line
            loaded_words = [line.strip() for line in lines]

        return(loaded_words)

    except FileNotFoundError:
        return []

def save_words_said(words):
    file_path = base_path + 'said_words.txt'
    with open(file_path, 'w') as f:
        for word in words:
            f.write(word + '\n')



def get_lexicon_list():
    file_path = base_path + 'lexicons/'
    lexicon_list = []
    if os.path.exists(file_path):
        for f in os.scandir(file_path):
            if f.is_file() and f.name.endswith(".lex"):
                lexicon_list.append(f.name[:-4])
    else:
        os.mkdir(file_path)

    return sorted(lexicon_list)


def load_lexicon(lexicon, loadList = True):
    file_path = base_path + 'lexicons/' + lexicon + ".lex"
    with open(file_path, 'r') as file:
        if loadList:
            loaded_list = json.load(file)
        else:
            loaded_list = file.read()[1:-1]
        return loaded_list


def save_lexicon(name, lexicon_string):
    file_path = base_path + 'lexicons/' + name + '.lex'
    lexicon_list = json.loads("[" + lexicon_string + "]")

    #Remove non-unique elements
    unique_elements = set(lexicon_list)
    lexicon = list(unique_elements)

    with open(file_path, 'w') as file:
        json.dump(lexicon, file)


def import_lexicon(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


    #Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = file_content.translate(translator)
    word_list = cleaned_text.split()

    #Remove non-unique elements
    unique_elements = set(word_list)
    lexicon = list(unique_elements)
    return json.dumps(lexicon)[1:-1]

def new_lexicon():
    file_path = base_path + 'lexicons/'

    lexicon_name = "new_lexicon"
    counter = 1

    blank_lexicon = "[]"

    if os.path.exists(file_path + lexicon_name + ".lex"):
        while os.path.exists(file_path+"new_lexicon"+str(counter)+".lex"):
            counter += 1

        lexicon_name = "new_lexicon" + str(counter)
        with open(file_path + lexicon_name + ".lex", 'w') as file:
            file.write(blank_lexicon)

    else:
        with open(file_path + lexicon_name + ".lex", 'w') as file:
            file.write(blank_lexicon)

    return lexicon_name

def delete_lexicon(name):
    file_path = base_path + 'lexicons/'
    if os.path.exists(file_path + name + ".lex"):
        os.remove(file_path + name + ".lex")
