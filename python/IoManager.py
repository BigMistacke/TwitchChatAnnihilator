import json
import os

def load_tokens():
    if os.path.exists('tokens.json'):
        with open('tokens.json', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                # File is empty or invalid JSON
                return {}
    else:
        return {}

def save_tokens(tokens):
    with open('tokens.json', 'w') as file:
        json.dump(tokens, file)


def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                # File is empty or invalid JSON
                return {}
    else:
        return {}

def save_settings(settings):
    with open('settings.json', 'w') as file:
        json.dump(settings, file)

def retrieve_rule_list():
    rule_list = []
    if os.path.exists("./rules"):
        for f in os.scandir("./rules"):
            if f.is_file() and f.name.endswith(".tca"):
                rule_list.append(f.name[:-4])
    else:
        os.mkdir("./rules")

    return sorted(rule_list)

def retrieve_rule(name):
    if os.path.exists("./rules/"+name+".tca"):
        with open("./rules/"+name+".tca", 'r') as file:
            return file.read()


def save_rule(name, rule):
    with open("./rules/"+name+".tca", 'w') as file:
        return file.write(rule)

def delete_rule(name):
    if os.path.exists("./rules/"+name+".tca"):
        os.remove("./rules/"+name+".tca")


def new_rule():
    rule_name = "new_rule"
    counter = 1

    blank_rule = """timeout 5 cooldown 0: [

]"""

    if os.path.exists("./rules/"+rule_name+".tca"):
        while os.path.exists("./rules/"+rule_name+str(counter)+".tca"):
            counter += 1

        rule_name = rule_name + str(counter)
        with open("./rules/"+rule_name+".tca", 'w') as file:
            file.write(blank_rule)

    else:
        with open("./rules/"+rule_name+".tca", 'w') as file:
            file.write(blank_rule)

    return rule_name


def load_messages_said():
    loaded_messages= []

    try:
        with open("said_messages.txt", 'r') as f:
            # Read all lines from the file
            lines = f.readlines()

            # Strip the newline character from each line
            loaded_messages = [line.strip() for line in lines]

        return(loaded_messages)

    except FileNotFoundError:
        return []

def save_messages_said(messages):
    with open("said_messages.txt", 'w') as f:
        for message in messages:
            f.write(word + '\n')

def load_words_said():
    loaded_words = []

    try:
        with open("said_words.txt", 'r') as f:
            # Read all lines from the file
            lines = f.readlines()

            # Strip the newline character from each line
            loaded_words = [line.strip() for line in lines]

        return(loaded_words)

    except FileNotFoundError:
        return []

def save_words_said(words):
    with open("said_words.txt", 'w') as f:
        for word in words:
            f.write(word + '\n')

