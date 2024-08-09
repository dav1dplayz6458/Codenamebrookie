<div align="center">
  <img src="https://github.com/DanielOrourke02/Echo/blob/main/images/bot_icon.png" alt="Echo Bot Image" width="400">
</div>

<h1 align="center">
  <br>
  Echo Bot v5
  <br>
</h1>

<p align="center">Admin, AutoMod, Economy, Fun, Invite, Information, Moderation, Owner, Social, Suggestion, Tickets, verify, Utility and More...</p>

<br>

<p align="center">
  <a href="#-resource-links">Resource Links</a>
  •
  <a href="#-prerequisites">Prerequisites</a>
  •
  <a href="#-getting-started">Getting Started</a>
</p>

<br>

~~# MAJOR UPDATE, MOVED TO SQL DATABASES~~

## ⭐Plans for the next major update⭐

- Move to slash commands (pycord)
- UI interactions (buttons)
- Interactive tutorial/better tutorial

## 🔗 Resource Links

- 🤖 LIVE BOT: [Echo](https://top.gg/bot/1075434463217066014) Now on Top.gg!
- 🤝 Support Server: [Join Here](https://discord.gg/kNWkT8xWg6)
- 🤝 Hire me: [Join Here](https://discord.gg/kNWkT8xWg6) or dm `mal023`
- 📂 Documentation URL: comming soon

## 📦 Prerequisites

- [Python3.12](https://www.python.org/downloads/release/python-3120/)
  - [Python install help](https://www.youtube.com/watch?v=nU2Egc3Zx3Q) 
- [Git](https://git-scm.com/downloads)
- [Windows](https://www.microsoft.com/en-gb/windows) or [Linux](https://ubuntu.com/)

## 🚀 Getting Started

> [!WARNING]
> Untested on MAC-OS

## Windows Installation

- Open command prompt (cmd.exe) and run the following commands

```
git clone https://github.com/DanielOrourke02/Echo
cd Echo
python -m venv venv
venv\Scripts\activate
pip install -r \src\databases\requirements.txt
```

- Open the cloned directory in windows file explorer

- Open config.json and add the following values

  - Your Bot Token (essential)
  - Your Bot Invite Link (optional)
  - Your User ID (optional)

- Now back to your terminal and run win_run.bat inside the terminal with the venv activated. (this is essential)

```
.\win_run.bat
```

## Linux Installation

- Open the terminal and run the following commands:

```
git clone https://github.com/DanielOrourke02/Echo
cd Echo
python3 -m venv venv
source venv/bin/activate
pip install -r src/databases/requirements.txt
```
- Now open config.json (in the terminal), or open it in notepad++ if you prefer.

```
nano config.json
```

- Add the following data to config.json:

  - Your Bot Token (essential)
  - Your Bot Invite Link (optional)
  - Your User ID (optional)

- After that run the following commands to run the bot:

```
chmod +x linux_run.sh
./linux_run.sh
```

<h2 align="center">
  <br>
  Connect with me
  <br>
</h2>

<p align="center">Hire Me: https://discord.gg/kNWkT8xWg6 Or DM ME: mal023</p>

## General Commands

| Command                   | Description                                      |
|---------------------------|--------------------------------------------------|
| `help`                    | Get help for commands.                           |
| `economy`                 | List economy commands.                           |
| `moderation`              | Get help for moderation commands (Admin only).   |
| `ping`                    | Get the bot's current latency.                   |
| `say <message>`           | Repeat a message.                                |
| `coinflip <heads/tails`   | Flip a coin.                                     |
| `avatar <@user>`          | Output a users avatar                            |
| `dice`                    | Roll a six-sided die.                            |
| `8ball <question>`        | Ask an 8ball a question.                         |
| `quote`                   | Get a daily quote from an API.                   |
| `qr <text/link>`          | Generate a QR code from a link.                  |
| `membercount`             | Get the member count of the server.              |
| `calculator <+-*/>`       | Perform basic calculations.                      |
| `joke`                    | Get a random joke.                               |
| `user_info <@user>`       | Get info on a user                               |
| `server_info`             | Get the servers info                             |

## Economy Commands

| Command                  | Description                                           |
|--------------------------|-------------------------------------------------------|
| `balance`                | Checks your current bank and pocket balance.          |
| `networth`               | Checks your total networth (assets included)          |
| `baltop`                 | Displays the richest people leaderboard (networth)    |
| `tutorial`               | A tutorial command (economy game only rn)             |
| `daily`                  | Claims your daily reward.                             |
| `shop`                   | Views available items in the shop.                    |
| `trade <@user> <item_id>`| Gives an item to a player.                            |
| `cosmetics`              | Lists available cosmetics and their prices.           |
| `buy <item_id>`          | Buys an item from the shop.                           |
| `sell <item_id>`         | Sells an item for its value.                          |
| `beg`                    | Beg for money.                                        |
| `hunt`                   | hunt for cosmetics and money. (with a bow)            |
| `dig`                    | Dig for cosmetics and money. (with a shovel)          |
| `scrap`                  | Find cosmetics and money.                             |
| `shoot <@user>`          | Shoot a user with a gun or a M4A1                     |
| `bomb <@user>`           | Bomb a user with C4                                   |
| `inventory`              | Lists items in your inventory.                        |
| `pay <amount>`           | Pay someone money.                                    |
| `deposit <amount/max>`   | Deposit money into your bank (earns interest).        |
| `withdraw <amount/max>`  | Withdraw money from your bank.                        |
| `rob <@user>`            | Rob a user and potentially steal some of their money. |
| `plant <amount/max>`     | Plant crops to sell later at a profit.                |
| `harvest`                | Harvest your planted crops.                           |
| `craft <recipe_name>`    | Craft items.                                          |
| `recipes`                | Shows craftable items and required materials.         |
| `gamble <amount>`        | Gamble your money with a 1/3 chance of winning.       |
| `blackjack <amount>`     | Play a cool interactive blackjacks game.              |
| `slots <amount>`         | Play slots with a small chance of winning big.        |

## Moderation Commands

| Command             | Description                                      |
|---------------------|--------------------------------------------------|
| `kick <@user> <reason>` | Kick a user from the server.                 |
| `ban <@user> <reason>`  | Ban a user from the server.                  |
| `mute <@user> <reason>` | Mute a user in the server.                   |
| `unmute <@user> <reason>` | Unmute a user in the server.               |
| `clear <amount>`        | Clear a specified number of messages in a channel. |
| `ticketpanel <message>` | Create a ticket panel for support.           |
| `setup-verify <role_name> <message>` | Set up a verification panel.    |
| `lockchannel`       | Lock a channel for a specified duration.         |
| `unlockchannel`     | Unlock a channel.                                |
| `lockserver`        | Lock the entire server for a specified duration. |
| `unlockserver`      | Unlock the entire server.                        |
| `config_view`       | Read config.json from discord (admin id only)    |
| `config_edit <varialbe> <new_value>` | Edit config.json from discord.  |

## Shop (ingame)

| Item   | Description                                | Cost  |
|--------|--------------------------------------------|-------|
| `Silver` | Bank full? Cant afford any gold? Buy some silver                              | 1000  |
| `Gold`   | Too rich? Banks full? Invest some money into gold. No interest, but its safe. | 10000 |
| `shovel` | Dig up treasure, find items and make money!                                   | 1000  |
| `bow`    | You can now hunt animals! Sell what you find and make money while doing it.   | 1000  |


## Craftable Items (ingame)

| Item               | Ingredients                                  | Description                                      |
|--------------------|----------------------------------------------|--------------------------------------------------|
| `Excalibur`         | 2 guns, 1 mythical_sword                      | A powerful sword that only the one can handle  |
| `M4A1`              | 2 guns, 1 stick                               | Shoot down your enemies                        |
| `8_Incher`          | 1 stick, 1 david4                             | A unique and 8 inch weapon                     |
| `Complete_Gauntlet` | 1 infinity, 1 leg.sword, 1 david4             | The most powerful item in the game             |
| `C4`                | 2 sulphur, 1 charcoal, 1 clock, 5 potatoes, 2 tech | C4 Bomb for bombing people                |
| `Poo`               | 3 charcoal, 1 sulphur                         | Just poo                                       |
| `Joint`             | 1 roll, 1 weed                                | Sell joints                                    |
| `meth`              | 1 chemical, 1 red, create using `!cook`       | sell meth by using `!streets`                  |
| `glitch`             |2x god (0.1% chance for each)                 | A glitch in the matrix                         |

## Findable Items (ingame)

I call them 'cosmetics', but they are items you get from running: dig, hunt and scrap. These items can be used to craft items that sell for more e.g Joint, C4

| Item             | Description                     | Sell Value | Chance (%) |
|------------------|---------------------------------|------------|-------------|
| `Rare Sword`       | Rare Sword                      | 2500       | 25          |
| `Legendary Sword`  | Legendary Sword                 | 5000       | 15          |
| `Mythical sword`   | Mythical sword                  | 12500      | 5           |
| `god`              | An item that only the gods can hold | 15000000 | 0.1       |
| `Shovel`           | Shovel used for digging         | 1000       | 23          |
| `Bow`              | Bow used for hunting            | 1000       | 20          |
| `Infinity Gauntlet`| Infinity Gauntlet               | 30000      | 5           |
| `David's 4th ball` | David's 4th ball                | 25000      | 7           |
| `Stick`            | Stick                           | 15000      | 15          |
| `Glock-18`         | Glock-18                        | 8000       | 19          |
| `Weed`             | Weed                            | 5000       | 30          |
| `Sulphur`          | Sulphur                         | 500        | 40          |
| `Charcoal`         | Charcoal                        | 300        | 50          |
| `Alarm Clock`      | Alarm Clock                     | 700        | 30          |
| `Roll`             | Roll paper for weed             | 1500       | 33          |
| `Potato`           | Potato                          | 100        | 65          |


<div align="center">
  <img src="https://github.com/DanielOrourke02/Active-Projects/blob/main/images/Visual_Studio_Icon_2019.svg.png" width="48" height="48" alt="Visual Studio" />
  <img src="https://github.com/DanielOrourke02/Active-Projects/blob/main/images/python.png" alt="Python" />
  <img src="https://github.com/DanielOrourke02/Active-Projects/blob/main/images/html.png" alt="HTML" />
  <img src="https://github.com/DanielOrourke02/Active-Projects/blob/main/images/css.png" alt="CSS" />
  <img src="https://github.com/DanielOrourke02/Active-Projects/blob/main/images/C%2B%2B.png" alt="C++" />
  <img src="https://github.com/DanielOrourke02/Active-Projects/blob/main/images/linux.png" alt="Linux" />
</div>
