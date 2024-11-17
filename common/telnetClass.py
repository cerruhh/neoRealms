import string
import telnetlib
import json
import re

from colorama import Fore
from time import sleep as wait
import common.get_user_info
import common.shop_lists
import os

is_nt = os.name == "nt"
is_linux = os.name == "linux"
writeapitofile = False


def TurnFull(cmd: str):
    if cmd == "n":
        # print(Fore.MAGENTA + storage.art.movedn)
        return "north"
    elif cmd == "s":
        # print(Fore.MAGENTA + storage.art.moveds)
        return "south"
    elif cmd == "e":
        # print(Fore.MAGENTA + storage.art.movede)
        return "east"
    elif cmd == "w":
        # print(Fore.MAGENTA + storage.art.movedw)
        return "west"


class realmsClient:
    def __init__(self, password: str, usrname: str, dbglv: int = 0):
        """
        init fucn
        :param password:
        :param usrname:
        """

        self.telnetClient = telnetlib.Telnet()
        self.password = password
        self.username = usrname
        self.exited = False
        if dbglv != 0:
            self.telnetClient.set_debuglevel(dbglv)
        self.current_room = ""

    def connect(self):
        """
        connect to realms93 servers and automatically login using given credentials
        :return:
        """
        self.telnetClient.open(host="windows93.net", port=8082)
        self.telnetClient.read_until(b'Please enter your name, or "new" if you are new.')

        self.telnetClient.write(str.encode(self.username + "\n"))
        wait(0.1)
        self.telnetClient.write(str.encode(self.password + "\n"))
        print(bytes.decode(self.telnetClient.read_very_eager()))

        return self.telnetClient

    def get_api_dict(self) -> dict:
        """
        get the api dictionary provided by Realms93.
        :return:
        """
        while 1:
            print("attempt")
            self.telnetClient.write(str.encode("api\n"))
            wait(0.06)
            eagerlook = bytes.decode(self.telnetClient.read_very_eager(), encoding="utf-8")
            # , encoding="utf-8"
            last_line_eager = str.split(eagerlook, "\n")[-1].strip().replace("\n", "")
            ascii_ver = ''.join(filter(lambda x: x in string.printable, last_line_eager)).replace("0m", "")
            if eagerlook == "":
                continue
            if eagerlook[0] == "[" and eagerlook[-1] != "]":
                ascii_ver += "]"
            if eagerlook[0] == "[" or eagerlook[0] == "{":
                try:
                    eval(eagerlook.strip())
                except SyntaxError:
                    continue
                dictver = eval(eagerlook.strip())
                if not dictver:
                    continue

                if writeapitofile:
                    with open(file="storage/apistore.json", mode="w", newline=None) as apifile:
                        json.dump(dictver, apifile, indent=3)
                if dictver is list:
                    if len(dictver) == 0:
                        continue
                    return dictver[0]
                else:
                    return dictver
            else:
                continue

    def run_alias(self, aliascmd: str):
        """
        run an alias set in accountdata.json
        :param aliascmd:
        :return:
        """
        accinfo = common.get_user_info.getUserCond()
        if len(accinfo["aliases"]) != 0:
            if aliascmd == "lists":
                print(common.shop_lists.list_all)
            if aliascmd.split(" ")[0] == "list" and len(aliascmd.split(" ")) == 2:
                shopval = None
                try:
                    shopval = common.shop_lists.shoplist[str(aliascmd.split(" ")[1].strip())]
                except KeyError:
                    print("Shop Not Found, type lists for all shop lists.")
                print("ShopVal")
                return shopval
            if aliascmd == "man":
                if is_nt:
                    print("NT detected, attempting to open README in notepad...")
                    os.system("notepad ..\\README.md")
                    with open(file="../README.md", mode="r") as txt:
                        read_txt = txt.read()
                        print(Fore.RED + read_txt)
                elif is_linux:
                    print("Linux Detected, Attempting to open README in nano...")
                    with open(file="../README.md", mode="r") as txt:
                        read_txt = txt.read()
                        print(Fore.RED + read_txt)
                        print(Fore.LIGHTYELLOW_EX)

                    os.system('/bin/bash -c $"nano ..\\README.md"')

            for cmd in accinfo["aliases"]:
                split = str.split(cmd, "|")
                if split[0] == aliascmd:
                    self.send_message(split[1])

    def take_all_money(self, apiparam: dict = None):

        """
        take all money from ground
        :return:
        :param: apiparam
        """
        api = None
        if apiparam is not None:
            api = apiparam
        else:
            api = self.get_api_dict()
        room_money = api["room"]["money"]
        if room_money != 0:
            self.telnetClient.write(str.encode("take $" + str(room_money)))
            newapi = self.get_api_dict()
            return room_money

    def send_message(self, inputx: str, isrecall: bool = False, api: dict = None):
        """
        send a command to telnet.
        :param isrecall:
        :param api:
        :param inputx:
        :return:
        """

        if inputx == "quit":
            self.exited = True
            self.telnetClient.close()
            print(Fore.RED + "Connection Closed to windows93.net:8082")
            exit(0)

        vapi = None
        if api is not None:
            vapi = api
        else:
            vapi = self.get_api_dict()

        if inputx == "l" or inputx == "look":
            self.print_look(apiparam=vapi)
            return False

        if inputx == "n" or inputx == "w" or inputx == "e" or inputx == "s":
            if inputx not in vapi["room"]["exits"]:
                print(Fore.MAGENTA + "You cannot bump into walls.")
                return False
            else:
                self.telnetClient.write(str.encode(TurnFull(cmd=inputx) + "\n"))
                wait(0.2)
                #                self.print_look()
                return True

        if "fuck" in inputx:
            wants_hell = input(
                Fore.RED + "Are you sure you want to go to hell? (saying fuck will teleport you to hell)? \n (Y/N) > ")
            if wants_hell.lower() == "y":
                self.telnetClient.write(str.encode(inputx + "\n"))
                return False
            else:
                self.telnetClient.write(str.encode(inputx.replace("fuck", "funk") + "\n"))
                return False
        else:
            self.telnetClient.write(str.encode(inputx + "\n"))

            return False

    def auto_attack(self, api: dict = None):
        """
        automatically attack
        :param api:
        :return:
        """
        api_req = None
        if None != api:
            api_req = api
        else:
            api_req = self.get_api_dict()

        weapon_attack_speed = common.get_user_info.getUserCond()["attack_speed"]
        if len(api_req["room"]["enemies"]) != 0:
            while True:
                self.telnetClient.write(str.encode("a\n"))
                wait(weapon_attack_speed)

    def print_latest(self):
        """
        print latest
        :return:
        """
        # print(bytes.decode(self.telnetClient.read_very_eager()))
        print(bytes.decode(self.telnetClient.read_very_eager()))

    def print_look(self, apiparam: dict = None):
        """
        getting a look at the place the player currently recides
        :return:
        """

        exitNodes = ""
        enemylist = ""
        humanlist = ""
        itemlist = ""
        apireq = None
        if apiparam is not None:
            apireq = apiparam
        else:
            apireq = self.get_api_dict()

        if "n" in apireq["room"]["exits"]:
            exitNodes += "NORTH "
        if "e" in apireq["room"]["exits"]:
            exitNodes += "EAST "
        if "w" in apireq["room"]["exits"]:
            exitNodes += "WEST "
        if "s" in apireq["room"]["exits"]:
            exitNodes += "SOUTH "

        for i in apireq["room"]["enemies"]:
            enemylist += i + " "

        for i in apireq["room"]["players"]:
            humanlist += i + " "
        for i in apireq["room"]["items"]:
            itemlist += i + " "

        exitNodes.strip()
        print(Fore.WHITE + apireq['room']['name'])
        print(Fore.MAGENTA + str.replace(apireq['room']['description'], "<", "[").replace(">", "]"))
        print(Fore.YELLOW + "exits:" + exitNodes)
        if itemlist != "":
            print(Fore.LIGHTYELLOW_EX + f"You see: {itemlist}")
        if humanlist != "":
            print(Fore.CYAN + f"People: {humanlist}")
        if enemylist != "":
            print(Fore.RED + f"Enemies: {enemylist}")

    def infiniatk(self):
        """
        infintly attacks
        :return:
        """
        extrax = Extras
        isLast = 0
        accinfo = common.get_user_info.getUserCond()
        while True:
            pass
            self.send_message("a")
            if accinfo["attack_speed"]<0.1:
                print("atk speed smaller than ms-latency, setting to 0.1")
                accinfo["attack_speed"]=0.1

            wait(accinfo["attack_speed"])
            print(f"Current Atk Speed: {accinfo['attacks_speed']}")
            if not accinfo["aaf_dont_take_money"]:
                self.take_all_money()
            # api = client.get_api_dict()
            # curlv=api["level"]
            # xpNeeded=extrax.next_level_exp(lv=curlv) - api["experience"]
            # client.send_message("a", api=api)
            # latest=client.print_latest()
            # eager=Fore.RED+bytes.decode(client.telnetClient.read_very_eager())
            # if eager!="\n":
            #     print(Fore.RED+bytes.decode(client.telnetClient.read_very_eager()))
            # if isLast!=xpNeeded:
            #     print(Fore.LIGHTRED_EX+f"You need {xpNeeded} to get to the next level!")
            #     isLast=xpNeeded
            # wait(0.2)


class Extras:
    def __init__(self):
        pass

    @staticmethod
    def next_level_exp(lv: int):
        """
        get the amount of xp required for specified level
        :param lv:
        :return:
        """
        return round(100 * (pow(1.4, lv) - 1))

    @staticmethod
    def get_all_accs(self):
        userCond = common.get_user_info.getUserCond()
        return userCond["accounts"]
