import random
import time

class Config:
    def __init__(self, timeout, cooldown, reason, condition):
        self.timeout = timeout
        self.cooldown = cooldown
        self.condition = condition
        self.reason = reason
        self.last_timeout = 0

    def evaluate(self, message):
        if(time.time() - self.last_timeout > self.cooldown):
            if self.condition == None:
                self.last_timeout = time.time()
                return True, self.timeout, self.reason
            elif self.condition.evaluate(message):
                self.last_timeout = time.time()
                return True, self.timeout, self.reason

        return False, self.timeout, self.reason



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
