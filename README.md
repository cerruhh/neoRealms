
# NeoRealms
A custom Realms client designed to customize & improve the Realms93 experience.



## Installation

debian:
```bash
sudo apt install python3 pip pip3 pipx
pip install colorama
git clone https://github.com/cerruhh/neoRealms.git
cd neoRealms
python3 main_selection.py
```

arch:

```bash
sudo pacman -Syu python3 pip pip3 pipx
pip install colorama
git clone https://github.com/cerruhh/neoRealms.git
cd neoRealms
python3 main_selection.py
```

Windows: Find Python on the internet and install it, then download NeoRealms. Run main_selection.py


## Configuration
in common/accountdata.json you can find the configuration, here is a example followed by instructions to configure NeoRealms:

```json
{
  "info": {
    "password": "userpassword",
    "username": "username",
    "attack_speed": 1,
    "host":"https://windows93.net"
    "port":8082
    "aliases": [
      "run townsquare-christiana|run 3n2e4n2e1n1e3n1e4n1w3n1w2n1w1n1w1n2w1n2w1n1w",
      "run christiana-townsqaure|run 1e1s2e1s2e1s1e1s1e2s1e3s1e4s1w3s1w1s2w4s2w3s",
      "_testalias93|test_api aliaskit93",
      "s|south",
      "n|north",
      "w|west",
      "e|east",
      "iha|hello everyone! i will let you know that i have no life whatsoever!"
    ]
  }
}

```

most configurations should be obvoius. In case of the aliases do: "the alias|the command", use the | sign to seperate the alias and command. you can use aliases by running !alias_name. Setting "host" and "port" to empty will default to windows93.net and 8082.
