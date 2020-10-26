# BigManage
A discord bot designed to manage channel permissions and moderation in a scalable form

# Setup
Currently I am building this bot in Python 3.8, but there is compatability with 3.6+.
The dependencies can be installed with `pip install -r requirements.txt` (Might need sudo).
A file named `.bot_token` will be created by running `BM_GenerateToken.py` with python and giving it the token found in the discord developer portal, alternatively you can run main.py and if it detects no tokenfile you will be prompted to make one.
After all this is done main.py needs to be executed using Python

# Features

## Bot Based Messages
Send and edit messages by the bot, so any administrator can edit the message sent, not just the one who originally wrote it.

## Bulk Channel Role Distribution
Manage large amounts of channels and roleperms by grouping channels into channel groups and treating their permissions as one channel, potentially saving hours of adding a new role, like a moderator role, to all the channels individually.
