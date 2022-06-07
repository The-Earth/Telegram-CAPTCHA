# Telegram-CAPTCHA

A Telegram CAPTCHA bot for group entry. It is derived from [fossifer's design](https://github.com/fossifer/Telegram-CAPTCHA-bot) and written with [catbot](https://github.com/The-Earth/catbot). In addition to fossifer's original design, ability of running in large groups (with no explicit joining messages) and blocking spam usernames are added.

## Installation

```bash
git clone https://github.com/The-Earth/Telegram-CAPTCHA
cd Telegram-CAPTCHA
pip install -r requirements.txt
cp config_example.json config.json
```

Then edit `config.json`, fill in bot token, set username blacklist, add messages for your language and put the language code in to language list (optional).

```bash
nohup python3 main.py &
```

## Known issue

The bot will completely mute the user who has previous restriction by other admins after passing their CAPTCHA. If the previous restriction was a partial mute (that the user could send basic text while be banned from some types of messages), this could be undesirable.
