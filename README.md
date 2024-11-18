
# NeoRealms
A custom Realms client designed to customize & improve the Realms93 experience.



## Installation

Debian/Ubuntu:

sh:
```bash
sudo apt install python3 pip pipx git 
sudo pip install colorama
git clone https://github.com/cerruhh/neoRealms.git ~/neoRealms
cd ~/neoRealms
python ./main_selection.py
```

Arch:

sh:
```bash
sudo pacman -Syu python3 python-pip git python-colorama
git clone https://github.com/cerruhh/neoRealms.git ~/neoRealms
cd ~/neoRealms
python main_selection.py
```

Windows 11 (Elevated):
Required administrative privliges.

Powershell:
```ps1
winget install -e --id Python.Python.3.11
winget install -e --id Git.Git
git clone https://github.com/cerruhh/neoRealms.git ~\neoRealms
cd ~\neoRealms
python neoRealms
```

The commands above can be replicated on all distributions supporting python.

## Configuration
in common/accountdata.json you can find the configuration, here is an example followed by instructions to configure NeoRealms:

```json
{
  "info": {
    "username": "mainusername",
    "password": "mainpassword",
    "attack_speed": 5,
    "host":"windows93.net",
    "port":8082,
    "debug_level": 0,
    "aaf_dont_take_money": false,
    "welcome_art": 1,
    "accounts": [
      {
          "username": "example_alt_account_username",
          "password": "example_alt_account_password"
      }
    ],
    "delay": 0.2,
    "aliases": [
      "run tq-ch|run 3n2e4n2e1n1e3n1e4n1w3n1w2n1w1n1w1n2w1n2w1n1w",
      "run ch-tq|run 1e1s2e1s2e1s1e1s1e2s1e3s1e4s1w3s1w1s2w4s2w3s"
    ]
  }
}

```

### Macros
Macros can be used to automate tasks defined in the configuration, here is an example:
```
aliasname|aliascommand
```
alias name is the command typed by the user, and aliascommand is the command sent to server when the macro is executed. you can use \n to put multiple commands totogether.
You can use macros to e.g. make run patterns, as shown in the example configuration file.

!aliasname will now run aliascommand into the terminal like this:
```
!aliasname
testuser says: aliascommand
```

### different host/port
you can change the host neoRealms is connecting to by changing "host" and "port" in accountsdata.json

### attack speed
you can change auto attack speed by changing "attack_speed" in your accountdata.json

### autologin
entering login credentials to "username" and "password" will automatically log you in to Realms93.

### chestmanager
the accouts section can add chest users to your account login at start of connection
login by typing
```
c -d
```


### Cusotmize your welcome ascii art
You can find all the ascii art under storage/art.py
You can customize this screen by changing the string.


### autocollect autocollect money
The client will automatically collect money when entering a room.
you can manually collect all money off the ground with the command `!col`.

You can toggle autocollect with the following command `!autocollect`.
You can figure out in what state autocollect is in with `!autocolst`.



### delay
The delay between each message to the server, used to prevent buffering.
The default 0.2 is 200ms, a good amount of delay without stability issues.


### shop lists
You can find the items sold on a shop without visiting the requested shop.
You can find the list of shops with !lists

you can get a shop with the !list command, e.g.
`!list jk`
would give you the shop items of joker keys