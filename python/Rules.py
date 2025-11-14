import random
import time

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

        for x in range(trials):
            for filter in self.filters:
                result = filter.test(message)

                #Only count timeouts to avoid problems due to user naming a rule "no timeout" or something stupid
                if result[0]:
                    message_counts.setdefault(result[2], 0)
                    message_counts[result[2]] += 1

        for message in message_counts:
            message_counts[message] = message_counts[message] * 100 / trials

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
        return all(cond.evaluate(message.body) for cond in self.conditions)


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


class Random:
    def __init__(self, probability):
        self.probability = probability

    def evaluate(self, message):
        return random.random() < self.probability
