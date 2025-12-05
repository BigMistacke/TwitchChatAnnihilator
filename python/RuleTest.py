from TwitchMessage import TwitchMessage
import Filter

from TwitchMessage import TwitchMessage

test_cases = [
    {
        "rules": '- contains["test"]',
        "ban_msg": TwitchMessage("A test message."),
        "pass_msg": TwitchMessage("No match here.")
    },
    {
        "rules": '- starts_with["OwO"]',
        "ban_msg": TwitchMessage("OwO UwU"),
        "pass_msg": TwitchMessage("UwU OwO")
    },
    {
        "rules": '- ends_with["UwU"]',
        "ban_msg": TwitchMessage("OwO UwU"),
        "pass_msg": TwitchMessage("UwU OwO")
    },
    {
        "rules": '- regex["j.b"]',
        "ban_msg": TwitchMessage("job"),
        "pass_msg": TwitchMessage("joob")
    },


    {
        "rules": '- emotes[> 2]',
        "ban_msg": TwitchMessage(body="bing bang", emotes=3),
        "pass_msg": TwitchMessage(body="bing bang", emotes=1)
    },
    {
        "rules": '- punctuation[> 2]',
        "ban_msg": TwitchMessage("bing bang!!?"),
        "pass_msg": TwitchMessage("bing bong!?")
    },
    {
        "rules": '- length[> 10]',
        "ban_msg": TwitchMessage("Very very very long message"),
        "pass_msg": TwitchMessage("Short word")
    },
    {
        "rules": '- caps[> 0.5]',
        "ban_msg": TwitchMessage("ANGRY WORDS!"),
        "pass_msg": TwitchMessage("soft words")
    },
    {
        "rules": '- said_word[]',
        "ban_msg": TwitchMessage("bing bang"),
        "pass_msg": TwitchMessage("bing bong")
    },
    {
        "rules": '- said_message[]',
        "ban_msg": TwitchMessage("bing bang"),
        "pass_msg": TwitchMessage("bing bang")
    },



    {
        "rules": '- bits[> 5]',
        "ban_msg": TwitchMessage("Sinful donator", cheer=100),
        "pass_msg": TwitchMessage("Virtuous freeloader", cheer=0)
    },
    {
        "rules": '- mentions[< 2]',
        "ban_msg": TwitchMessage("Vile hermit", mentions=1),
        "pass_msg": TwitchMessage("Heavenly communicator", mentions=2)
    },



    {
        "rules": '- user_contains["Z"]',
        "ban_msg": TwitchMessage("Z-crew", username="Zalex"),
        "pass_msg": TwitchMessage("A-crew", username="alex")
    },
    {
        "rules": '- user_starts["A"]',
        "ban_msg": TwitchMessage("A-crew", username="Alex"),
        "pass_msg": TwitchMessage("Z-crew", username="Zalex")
    },
    {
        "rules": '- user_ends["Z"]',
        "ban_msg": TwitchMessage("Crew-Z", username="Alexaz"),
        "pass_msg": TwitchMessage("Crew-A", username="Alexa")
    },
    {
        "rules": '- role[moderator]',
        "ban_msg": TwitchMessage("Evil Mod", roles=["moderator", "VIP"]),
        "pass_msg": TwitchMessage("Blessed sub", roles=["sub", "VIP"]),
    },



    {
        "rules": '- any[contains["bing"], contains["bang"]]',
        "ban_msg": TwitchMessage("bing bong"),
        "pass_msg": TwitchMessage("oo wee")
    },
    {
        "rules": '- all[contains["bing"], contains["bang"]]',
        "ban_msg": TwitchMessage("bing bang"),
        "pass_msg": TwitchMessage("bing bong")
    },
    {
        "rules": '- none[contains["bing"], contains["bang"]]',
        "ban_msg": TwitchMessage("oo wee"),
        "pass_msg": TwitchMessage("bing bong")
    },
    {
        "rules": '- notall[contains["bing"], contains["bang"]]',
        "ban_msg": TwitchMessage("bing bong"),
        "pass_msg": TwitchMessage("bing bang")
    },
    {
        "rules": '- one[contains["bing"], contains["bang"]]',
        "ban_msg": TwitchMessage("bing wee!"),
        "pass_msg": TwitchMessage("bing bang")
    },
]


for i, case in enumerate(test_cases):
    rule = case["rules"]
    filter_func = Filter.create_filter(rule)

    print(case["rules"])
    print(filter_func.evaluate(case["pass_msg"]))
    print(filter_func.evaluate(case["ban_msg"]))
    print()

print("Testing complete.")
