
# NeoRealms
A custom Realms client designed to customize & improve the Realms93 experience.



## Installation

debian:
```bash
sudo apt install python3 pip git python-colorama
git clone https://github.com/cerruhh/neoRealms.git
cd neoRealms
python3 main_selection.py
```

arch:

```bash
sudo pacman -Syu python3 python-pip git python-colorama
git clone https://github.com/cerruhh/neoRealms.git
cd neoRealms
python3 main_selection.py
```

Windows: Find Python on the internet and install it, then download NeoRealms. Run main_selection.py
```bat
winget install git python


```


## Configuration
in common/accountdata.json you can find the configuration, here is a example followed by instructions to configure NeoRealms:

```json
{
  "info": {
    "password": "userpassword",
    "username": "username",
    "attack_speed": 1,
    "host":"https://www.windows93.net",
    "port":8082,
    "debug_level": 0,
    "accounts": [
      {
          "username": "us",
          "password": "pwd"  
      }
    ],
    "aliases": [
      "run townsquare-christiana|run 3n2e4n2e1n1e3n1e4n1w3n1w2n1w1n1w1n2w1n2w1n1w",
      "run christiana-townsqaure|run 1e1s2e1s2e1s1e1s1e2s1e3s1e4s1w3s1w1s2w4s2w3s",
      "_testalias93|test_api aliaskit93",
      "s|south",
      "n|north",
      "w|west",
      "e|east",
      "iha|hello everyone! i will let you know that i have no life whatsoever!",
      "wxx|l\n w\n"
    ]
  }
}

```


most configurations should be obvoius. In case of the aliases do: "the alias|the command", use the | sign to seperate the alias and command. you can use aliases by running !alias_name. Setting "host" and "port" to empty will default to windows93.net and 8082.


## Improvements & QoL changes
Here is what neoRealms does differently than https://windows93.net:8083.

- not entering movements if bumping into walls
- automatically taking money from ground.
- aliases to macro commands
- automatically attack enemies 24/7
- controlled swarm of synchronized users.
- alternate account manager

## How to use the Improvements.
### Macros
Macros can be used by typing ![aliasname]. aliases can be added to the accountinfo.json file.
aliases sytax is:
```
aliasname|aliascommand
```
!aliasname will now run aliascommand into the terminal like this:
```
!aliasname
testuser says: aliascommand
```

### different host
you can change the host neoRealms is connecting to by changing "host" and "port" in accountsdata.json

### attack_speed
you can change auto attack speed by changing "attack_speed"

### autologin
entering login credentials to "username" and "password" will automatically log you in to Realms93f

### chestmanager
the accouts section can add chest users to your account login at start of connection
login by typing
cli -d or c -d


### login type
cli / c (!-d)
opens as normal, (-d) to choose account
about / ab
shows about page, with the README
abort / abr
abort nr93
