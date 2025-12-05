from lark import Lark, Transformer, v_args
import Rules


def create_filter(rule):
    with open("grammar.lark") as f:
        grammar = f.read()

    parser = Lark(grammar, parser="lalr")
    tree = parser.parse(rule)

    transformer = TreeToObject()
    filter_tree = transformer.transform(tree)

    return filter_tree


@v_args(inline=True)
class TreeToObject(Transformer):

    def rules(self, *rules):
        return Rules.Start(list(rules))

    def config(self, timeout, cooldown, reason, condition=None):
        if timeout == None:
            timeout = 5
        if reason == None:
            reason = ""
        if cooldown == None:
            cooldown = 0
        return Rules.Config(timeout=int(timeout), cooldown=int(cooldown), reason=reason, condition=condition)

    def condition_list(self, *conditions):
        return list(conditions)

    #Logic
    def logic_condition(self, op, conditions):
        op_map = {
            "all": Rules.AllOf,
            "any": Rules.AnyOf,
            "none": lambda conds: Rules.Not(Rules.AnyOf(conds)),
            "notall": lambda conds: Rules.Not(Rules.AllOf(conds)),
            "one": Rules.ExactlyOne
        }
        return op_map[op](conditions)


    #Text match
    def contains_condition(self, *args):
        CONTAINS_MODES = {
            "any":    lambda message, targets: any(target in message for target in targets),
            "all":    lambda message, targets: all(target in message for target in targets),
            "none":   lambda message, targets: all(target not in message for target in targets),
            "notall": lambda message, targets: not all(target in message for target in targets),
            "one":    lambda message, targets: sum(1 for target in targets if target in message) == 1,
            "only":   lambda message, targets: all(word in targets for word in message.split())
        }

        evaluator = CONTAINS_MODES["any"]

        # Default cleaner (lowercase everything)
        cleaner = lambda message: message.lower()
        targets = []

        for arg in args:
            if isinstance(arg, list):
                targets = arg
            elif isinstance(arg, str):
                if arg in CONTAINS_MODES:
                    evaluator = CONTAINS_MODES[arg]
                elif arg == "strict":
                    # No cleaning
                    cleaner = lambda message: message

        cleaned_targets = [cleaner(target) for target in targets]
        return Rules.Contains(evaluator, cleaner, cleaned_targets)

    def starts_with_condition(self, *args):
        # Default cleaner (lowercase everything)
        cleaner = lambda message: message.lower()
        target = ""

        for arg in args:
            if arg == "strict":
                # No cleaning
                cleaner = lambda message: message
            else:
                target = arg


        cleaned_target = cleaner(target)
        return Rules.StartsWith(cleaner, cleaned_target)

    def ends_with_condition(self, *args):
        # Default cleaner (lowercase everything)
        cleaner = lambda message: message.lower()
        target = ""

        for arg in args:
            if arg == "strict":
                # No cleaning
                cleaner = lambda message: message
            else:
                target = arg


        cleaned_target = cleaner(target)
        return Rules.EndsWth(cleaner, cleaned_target)

    def regex_condition(self, regex):
        return Rules.RegexRule(regex)


    # Text element
    def caps_condition(self, comparison, target):
        COMPARISON_MODES = {
            ">":    lambda caps, target: caps >  target,
            "<":    lambda caps, target: caps <  target,
            "==":   lambda caps, target: caps == target,
            "!=":   lambda caps, target: caps != target
        }

        comparator = COMPARISON_MODES[comparison]
        return Rules.CapsCount(comparator, target)

    def length_condition(self, comparison, target):
        COMPARISON_MODES = {
            ">":    lambda message, target: len(message) > target,
            "<":    lambda message, target: len(message) < target,
            "==":   lambda message, target: len(message) == target,
            "!=":   lambda message, target: len(message) != target
        }

        comparator = COMPARISON_MODES[comparison]
        return Rules.LengthIs(comparator, target)

    def punctuation_condition(self, comparison, target):
        COMPARISON_MODES = {
            ">":    lambda count, target: count > target,
            "<":    lambda count, target: count < target,
            "==":   lambda count, target: count == target,
            "!=":   lambda count, target: count != target
        }

        comparator = COMPARISON_MODES[comparison]
        return Rules.PunctuationCount(comparator, target)

    def emote_count_condition(self, comparison, target):
        COMPARISON_MODES = {
            ">":    lambda emotes, target: emotes > target,
            "<":    lambda emotes, target: emotes < target,
            "==":   lambda emotes, target: emotes == target,
            "!=":   lambda emotes, target: emotes != target
        }

        comparator = COMPARISON_MODES[comparison]
        return Rules.EmoteCount(comparator, target)

    def word_said_condition(self, persistence, string_match, chance):
        # Default cleaner (lowercase everything)
        if string_match == None:
            cleaner = lambda message: message.lower()
        elif string_match == "strict":
            cleaner = lambda message: message

        if persistence == None:
            persistance = False

        if chance == None:
            chance = 1

        return Rules.AlreadySaidWord(cleaner, persistance, chance)

    def message_said_condition(self, persistence, string_match, chance):
        # Default cleaner (lowercase everything)
        if string_match == None:
            cleaner = lambda message: message.lower()
        elif string_match == "strict":
            cleaner = lambda message: message

        if persistence == None:
            persistance = False

        if chance == None:
            chance = 1

        return Rules.AlreadySaidMessage(cleaner, persistance, chance)



    #Message attributes
    def bit_condition(self, comparison, target):
        COMPARISON_MODES = {
            ">":    lambda bits, target: bits > target,
            "<":    lambda bits, target: bits < target,
            "==":   lambda bits, target: bits == target,
            "!=":   lambda bits, target: bits != target
        }

        comparator = COMPARISON_MODES[comparison]
        return Rules.BitsAre(comparator, target)

    def mention_condition(self, comparison, target):
        COMPARISON_MODES = {
            ">":    lambda mentions, target: mentions > target,
            "<":    lambda mentions, target: mentions < target,
            "==":   lambda mentions, target: mentions == target,
            "!=":   lambda mentions, target: mentions != target
        }

        comparator = COMPARISON_MODES[comparison]
        return Rules.MentionNumber(comparator, target)



    def random_condition(self, value):
        return Rules.Random(float(value))


    def role_condition(self, target):
        return Rules.HasRole(target)

    def user_contains_condition(self, *args):
        CONTAINS_MODES = {
            "any":    lambda message, targets: any(target in message for target in targets),
            "all":    lambda message, targets: all(target in message for target in targets),
            "none":   lambda message, targets: all(target not in message for target in targets),
            "notall": lambda message, targets: not all(target in message for target in targets),
            "one":    lambda message, targets: sum(1 for target in targets if target in message) == 1,
            "only":   lambda message, targets: all(word in targets for word in message.split())
        }

        evaluator = CONTAINS_MODES["any"]

        # Default cleaner (lowercase everything)
        cleaner = lambda message: message.lower()
        targets = []

        for arg in args:
            if isinstance(arg, list):
                targets = arg
            elif isinstance(arg, str):
                if arg in CONTAINS_MODES:
                    evaluator = CONTAINS_MODES[arg]
                elif arg == "strict":
                    # No cleaning
                    cleaner = lambda message: message

        cleaned_targets = [cleaner(target) for target in targets]
        return Rules.UserContains(evaluator, cleaner, cleaned_targets)


    def user_start_with_condition(self, *args):
        # Default cleaner (lowercase everything)
        cleaner = lambda message: message.lower()
        target = ""

        for arg in args:
            if arg == "strict":
                # No cleaning
                cleaner = lambda message: message
            else:
                target = arg


        cleaned_target = cleaner(target)
        return Rules.UserStartsWith(cleaner, cleaned_target)


    def user_ends_with_condition(self, *args):
        # Default cleaner (lowercase everything)
        cleaner = lambda message: message.lower()
        target = ""

        for arg in args:
            if arg == "strict":
                # No cleaning
                cleaner = lambda message: message
            else:
                target = arg


        cleaned_target = cleaner(target)
        return Rules.UserEndsWith(cleaner, cleaned_target)


    #Primatives
    def string_list(self, *strings):
        return [s.strip('"') for s in strings]

    def INT(self, tok):
        return int(tok)

    def FLOAT(self, tok):
        return float(tok)

    def STRING(self, tok):
        return str(tok)[1:-1]  # Remove quotes
