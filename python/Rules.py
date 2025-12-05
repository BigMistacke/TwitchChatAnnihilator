import random, time
import regex as re
import IoManager

said_words = []
said_messages = []

class Start:
    def __init__(self, filters):
        self.filters = filters

    def evaluate(self, message):
        for filter in self.filters:
            result = filter.evaluate(message)
            if(result[0] == True):
                return result

        return False, 0, "No timeout"


    def test(self, message, trials=1000):
        message_counts = {}
        total_misses = 100

        for x in range(trials):
            for filter in self.filters:
                result = filter.test(message)

                #Only count timeouts to avoid problems due to user naming a rule "no timeout" or something stupid
                if result[0]:
                    message_counts.setdefault(result[2], 0)
                    message_counts[result[2]] += 1

        for message in message_counts:
            total_misses = total_misses - message_counts[message] * 100 / trials
            message_counts[message] = message_counts[message] * 100 / trials

        # message_counts.setdefault("No timeout", total_misses)
        return message_counts


class Config:
    def __init__(self, timeout, cooldown, reason, condition):
        self.timeout = timeout
        self.cooldown = cooldown
        self.condition = condition
        self.reason = reason
        self.last_timeout = 0

    def evaluate(self, message):
        if(time.time() - self.last_timeout > self.cooldown):
            if self.condition == None or self.condition.evaluate(message):
                self.last_timeout = time.time()
                return True, self.timeout, self.reason

        return False, self.timeout, self.reason

    def test(self, message):
        if self.condition == None or self.condition.evaluate(message):
            return True, self.timeout, self.reason

        else:
            return False, 0, "No timeout"



# Logic Operators
class AllOf:
    def __init__(self, conditions):
        self.conditions = conditions

    def evaluate(self, message):
        return all(cond.evaluate(message) for cond in self.conditions)


class AnyOf:
    def __init__(self, conditions):
        self.conditions = conditions

    def evaluate(self, message):
        return any(cond.evaluate(message) for cond in self.conditions)

class ExactlyOne:
    def __init__(self, conditions):
        self.conditions = conditions

    def evaluate(self, message):
        return sum(cond.evaluate(message) for cond in self.conditions) == 1

#This doesn't exist in the grammar, but it's convient for changing AllOfs to notalls
class Not:
    def __init__(self, rule):
        self.rule = rule

    def evaluate(self, message):
        return not self.rule.evaluate(message)


# Message Text match
class Contains:
    def __init__(self, evaluator, cleaner, targets):
        self.evaluator = evaluator
        self.cleaner = cleaner
        self.targets = targets

    def evaluate(self, message):
        return self.evaluator(self.cleaner(message.body), self.targets)

class StartsWith:
    def __init__(self, cleaner, target):
        self.cleaner = cleaner
        self.target = target

    def evaluate(self, message):
        return self.cleaner(message.body).startswith(self.target)

class EndsWth:
    def __init__(self, cleaner, target):
        self.cleaner = cleaner
        self.target = target

    def evaluate(self, message):
        return self.cleaner(message.body).endswith(self.target)

class RegexRule:
    def __init__(self, regex):
        self.regex = regex

    def evaluate(self, message):
        return bool(re.search(self.regex, message.body))


# Message text elements
class EmoteCount:
    def __init__(self, comparator, target):
        self.comparator = comparator
        self.target = target

    def evaluate(self, message):
        return self.comparator(message.emotes, self.target)

class CapsCount:
    def __init__(self, comparator, target):
        self.comparator = comparator
        self.target = target

    def evaluate(self, message):
        message_len = len(message.body)

        if message_len == 0:
            self.comparator(self.target, 0)

        caps = sum(char.isupper() for char in message.body)
        return self.comparator(caps / message_len, self.target)

class PunctuationCount:
    def __init__(self, comparator, target):
        self.comparator = comparator
        self.target = target

    def evaluate(self, message):
        punctuation = re.findall(r'\p{P}', message.body)
        return self.comparator(len(punctuation), self.target)

class LengthIs:
    def __init__(self, comparator, target):
        self.comparator = comparator
        self.target = target

    def evaluate(self, message):
        return self.comparator(message.body, self.target)


class AlreadySaidMessage:
    def __init__(self, cleaner, isPersistent, probability):
        self.cleaner = cleaner
        self.isPersistent = isPersistent
        self.probability = probability

        if isPersistent:
            said_messages = IoManager.load_messages_said()

    def evaluate(self, message):
        if message.body in said_messages:
            return True

        else:
            if random.random() < self.probability:
                said_messages.append(message.body)
                if self.isPersistent:
                    IoManager.save_messages_said(said_messages)

            return False

class AlreadySaidWord:
    def __init__(self, cleaner, isPersistent, probability):
        self.cleaner = cleaner
        self.isPersistent = isPersistent
        self.probability = probability

        if isPersistent:
            said_words = IoManager.load_words_said()

    def evaluate(self, message):
        test_failed = False

        for word in message.body.split():
            if word in said_words:
                test_failed = True
            else:
                if random.random() < self.probability:
                    said_words.append(word)
                    if self.isPersistent:
                        IoManager.save_words_said(said_words)

        return test_failed



# Message attributes
class BitsAre:
    def __init__(self, comparator, target):
        self.comparator = comparator
        self.target = target

    def evaluate(self, message):
        return self.comparator(message.cheer, self.target)

class MentionNumber:
    def __init__(self, comparator, target):
        self.comparator = comparator
        self.target = target
    def evaluate(self, message):
        return self.comparator(message.mentions, self.target)



# User Information
class HasRole:
    def __init__(self, target):
        self.target = target

    def evaluate(self, message):
        return self.target in message.roles

class UserContains:
    def __init__(self, evaluator, cleaner, targets):
        self.evaluator = evaluator
        self.cleaner = cleaner
        self.targets = targets

    def evaluate(self, message):
        return self.evaluator(self.cleaner(message.username), self.targets)

class UserStartsWith:
    def __init__(self, cleaner, target):
        self.cleaner = cleaner
        self.target = target

    def evaluate(self, message):
        return self.cleaner(message.username).startswith(self.target)

class UserEndsWith:
    def __init__(self, cleaner, target):
        self.cleaner = cleaner
        self.target = target

    def evaluate(self, message):
        return self.cleaner(message.username).endswith(self.target)

# Misc
class Random:
    def __init__(self, probability):
        self.probability = probability

    def evaluate(self, message):
        return random.random() < self.probability
