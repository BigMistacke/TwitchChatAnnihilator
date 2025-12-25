# Twitch Chat annihilator
Finally, a way to randomly ban your chat for no reason at all!



## Rule Language Guide
The Twitch Chat Annihilator uses a custom language to define its rules. Each rule consists of optional settings, a separator (`-`), and a logical condition for the rule to time someone out.

### 📋 Rule Syntax
A rule is structured as follows:
`timeout DURATION_IN_SECONDS cooldown DURATION_IN_SECONDS reason "REASON" - CONDITION []`

* **timeout**: (Optional) Duration of the timeout, defaults to 5 seconds.  A timeout of 0 will result in a permanent ban.
* **cooldown**: (Optional) Minimum amount of time between activations of this rule, defaults to 0 seconds.
* **reason**: (Optional) Reason for the timeout given to the user.
* **condition**: The logic that must be met for the rule to ban someone. All conditions are written in the form CONDITION_NAME [ CONDITION_SETTINGS ]


---

### 🧠 Logic & Grouping
Multiple conditions can be grouped together in a rule in order to make a more complex set of conditions.  

| Operator | Description | Syntax |
| --- | --- | --- |
| `all` | All conditions must be true | `all[cond1, cond2]` |
| `any` | At least one condition must be true | `any[cond1, cond2]` |
| `none` | No conditions must be true | `none[cond1, cond2]` |
| `one` | Exactly one condition must be true | `one[cond1, cond2]` |
| `notall` | At least one condition must be false | `notall[cond1, cond2]` |

---

###  Content Matching Conditions
These rules look at the text of the message or the username.

#### **Contains**
* `contains[OP [MATCH] "word1", "word2", ...]` or `contains[[OP] [MATCH] lexicon "name"]`

Times out a user if their message matches the condition set in the rule. This operates on a letter level, so looking for "e" will look for ALL "e", not just whole words. 
**example**: `contains["apple", "orange", "pear"]`

There is a variant for checking the user's username instead of their message, using the same format and conditions.
`user_contains[[OP] [MATCH] word_list]`

**Operators (OP):** `all`, `any`, `none`, `one`, `only`.
**Match Types (MATCH):** `strict` (exact) or `loose` (case-insensitive).

#### **Other Matching conditions**
* `starts_with[[MATCH] "string"]`: Checks if the message begins with the string.
* `ends_with[[MATCH] "string"]`: Checks if the message ends with the string.
* `regex["pattern"]`: Matches against a Regular Expression.
* `user_starts[[MATCH] "string"]`
* `user_ends[[MATCH] "string"]`

---

### Quantitative Conditions
Use these to trigger rules based on numbers or percentages using comparison operators (`>`, `<`, `==`, `!=`).

| Condition | Unit | Example |
| --- | --- | --- |
| `length` | Character count | `length[> 100]` |
| `emotes` | Number of emotes | `emotes[> 5]` |
| `punctuation` | Number of marks | `punctuation[> 10]` |
| `caps` | Ratio of caps (0.0 - 1.0) | `caps[> 0.8]` |
| `bits` | Number of bits cheered | `bits[>= 100]` |
| `mentions` | Number of @users | `mentions[> 3]` |

---

### User & Meta Conditions
* `role[ROLE]`: Checks user status. Roles: `VIP`, `moderator`, `sub`.
* `random[FLOAT]`: Triggers based on probability (0.0 to 1.0). Example: `random[0.5]` is a 50% chance.

### Already Said
`said_word[[PERSISTENCE] [MATCH] [CHANCE]]]`
`said_message[[PERSISTENCE] [MATCH] [CHANCE]]`
These save all messages that are sent, and bans the user if the message has already been sent. 'said_word ' works on a word level and 'said_message' checks the entire message. 
**PERSISTENCE** is an optional parameter which allows you to save and load the list of said words/messages between sessions. It accepts values of "save" and "no_save".
**CHANCE** is an optional parameter which allows you to set a random chance (0.0 to 1.0) for the word/message to be added to the list of saved words/messages.
