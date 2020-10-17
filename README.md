# BigManage
A discord bot designed to manage channel permissions and moderation in a scalable form

# Setup
Currently I am building this bot in Python 3.8, but there is compatability with 3.6+.
The dependencies can be installed with `pip install -r requirements.txt` (Might need sudo).
A file named `.bot_token` will be created by running `encryptedtokengen.py` with python and giving it the token found in the discord developer portal.
After all this is done main.py needs to be executed using Python

# Features

## Bulk Channel Role Distribution
manage large amounts of channels with bulk role distribution that can be categorized and inherited from category, for example if you had a category `##games` with channels `#games-general`, `#minecraft`, and `#tetris` you can set so the `@minecraft` role gives +r acess to all the channels in category `##games` and then configure +w perms in `#minecraft` and `#games-general`, this skips having to manually set read perms to all 3 channels, because categories are not monolithic, you can also configure `##minecraft` group to include `#minecraft` and `#games-general` and just add +w perms to that group instead, and the bot will give the same output, using this modular design you can theoretically manage complex channel groups and permissions using simple categories
