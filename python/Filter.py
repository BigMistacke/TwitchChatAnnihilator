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
        return list(rules)

    def config(self, timeout, cooldown=0, reason="", condition=None):
        if reason == None:
            reason = ""
        return Rules.Config(timeout=int(timeout), cooldown=int(cooldown), reason=reason, condition=condition)

    def condition_list(self, *conditions):
        return list(conditions)

    def logic_condition(self, op, conditions):
        op_map = {
            "all": Rules.AllOf,
            "any": Rules.AnyOf,
            "none": lambda conds: Rules.Not(Rules.AnyOf(conds)),
            "notall": lambda conds: Rules.Not(Rules.AllOf(conds)),
            "one": Rules.ExactlyOne
        }
        return op_map[op](conditions)


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


    def string_list(self, *strings):
        return [s.strip('"') for s in strings]

    def random_condition(self, value):
        return Rules.Random(float(value))

    def INT(self, tok):
        return int(tok)

    def FLOAT(self, tok):
        return float(tok)

    def STRING(self, tok):
        return str(tok)[1:-1]  # Remove quotes
