import os
import json

template_settings = {
    "info": {
        "username": "example_username",
        "password": "example_password",
        "attack_speed": 1,
        "host": "windows93.net",
        "port": 8082,
        "debug_level": 0,
        "welcome_art": True,
        "small_welcome_art": True,
        "aaf_dont_take_money": False,
        "accounts": [
            {
                "username": "extra_account",
                "password": "secure_password#"
            }
        ],
        "delay":0.2,
        "aliases": [
            "example|run w1n2",
        ]
    }
}


def needs_setup():
    return os.path.exists("common/accountdata.json")


def setup():
    if not os.path.exists("common/accountdata.json"):
        xfile = open(file="common/accountdata.json", mode="x")
        xfile.close()

        with open("common/accountdata.json", mode="w") as file:
            json.dump(template_settings, file, indent=3)
            print("Settings File Created! Located at /common/accountdata.json")
