# sedlaif_bot
A python-telegram-bot that implements sed like behaviour and random text manipulation

Runs on telegram as [sedlaif_bot](https://t.me/sedlaif_bot).

## Starting the bot.

Once you've setup your configuration (see below) is complete, simply run:

`python3 -m sedlaif_bot`

### Configuration

Bot is configured using a config.py file

This file should be placed in your `sedlaif_bot` folder, alongside the `__main__.py` file . 
This is where your bot token will be loaded from.

An example `config.py` file could be:
```
class Config:
    API_KEY = "your bot api key"  # your api key, as provided by the botfather    
```

### Python dependencies

Install the necessary python dependencies by moving to the project root directory and running:

`sudo pip3 install -r requirements.txt`.

This will install all necessary python packages.

Have Fun!
