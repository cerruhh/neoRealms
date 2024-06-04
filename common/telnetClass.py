import string
import telnetlib
import json
import re

from colorama import Fore
from time import sleep as wait
import common.get_user_info
import storage.art

writeapitofile = False


def turnFull(cmd: str):
    if cmd == "n":
        print(Fore.MAGENTA + storage.art.movedn)
        return "north"
    elif cmd == "s":
        print(Fore.MAGENTA + storage.art.moveds)
        return "south"
    elif cmd == "e":
        print(Fore.MAGENTA + storage.art.movede)
        return "east"
    elif cmd == "w":
        print(Fore.MAGENTA + storage.art.movedw)
        return "west"


class realmsClient:
    def __init__(self, password: str, usrname: str,dbglv:int=0):
        """
        init fucn
        :param password:
        :param usrname:
        """

        self.telnetClient = telnetlib.Telnet()
        self.password = password
        self.username = usrname
        if dbglv != 0:
            self.telnetClient.set_debuglevel(dbglv)
        self.current_room = ""

    def connect(self):
        """
        connect to realms93
        :return:
        """
        self.telnetClient.open(host="windows93.net", port=8082)
        self.telnetClient.write(str.encode(self.username + "\n"))
        self.telnetClient.write(str.encode(self.password + "\n"))
        print(bytes.decode(self.telnetClient.read_very_eager()))

        return self.telnetClient

    def get_api_dict(self) -> dict:
        """
        get the api dictionary provided by Realms93.
        :return:
        """
        while 1:
            self.telnetClient.write(str.encode("api\n"))
            wait(0.01)
            eagerlook = bytes.decode(self.telnetClient.read_very_eager())
            last_line_eager = str.split(eagerlook, "\n")[-1].strip().replace("\n", "")
            ascii_ver = ''.join(filter(lambda x: x in string.printable, last_line_eager)).replace("0m", "")
            if eagerlook == "":
                continue
            if eagerlook[0] == "[" and eagerlook[-1] != "]":
                ascii_ver += "]"
            if eagerlook[0] == "[" or eagerlook[0] == "{":
                try:
                    dictver = eval(eagerlook.strip())
                except SyntaxError:
                    continue
                dictver = eval(eagerlook.strip())
                if dictver == []:
                    continue

                if writeapitofile:
                    with open(file="storage/apistore.json", mode="w", newline=None) as apifile:
                        json.dump(dictver, apifile, indent=3)
                if type(dictver) == list:
                    if len(dictver) == 0:
                        continue
                    return dictver[0]
                else:
                    return dictver
            else:
                continue

    def run_alias(self, aliascmd):
        """
        run an alias set in accountdata.json
        :param aliascmd:
        :return:
        """
        accinfo = common.get_user_info.getUserCond()
        if len(accinfo["aliases"]) != 0:
            for cmd in accinfo["aliases"]:
                split = str.split(cmd, "|")
                if split[0] == aliascmd:
                    self.send_message(split[1])

    def take_all_money(self, apiparam: dict=None):

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

    def send_message(self, inputx: str, api: dict=None):
        """
        send a command to telnet
        :param inputx:
        :return:
        """
        vapi = None
        if api is not None:
            vapi = api
        else:
            vapi = self.get_api_dict()

        if inputx == "quit":
            self.telnetClient.close()
            print(Fore.RED + "Connection Closed to windows93.net:8082")
            exit(0)

        if inputx == "l" or inputx == "look":
            self.print_look()
            return 0


        if inputx=="n" or inputx=="w" or inputx=="e" or inputx=="s":
            if inputx not in vapi["room"]["exits"]:
                print(inputx)
                print(Fore.MAGENTA + "You cannot bump into walls.")
                return 0
            else:
                print("runx")
                self.telnetClient.write(str.encode(turnFull(cmd=inputx) + "\n"))
                return 0

        if inputx == "list":
            readx = bytes.decode(self.telnetClient.read_until())
#           str.encode("--------------------------------------------------------------------------------")))

        if "fuck" in inputx:
            wants_hell = input(Fore.RED + "Are you sure you want to go to hell? (saying fuck will teleport you to hell)? \n (Y/N) > ")
            if wants_hell == "Y":
                self.telnetClient.write(str.encode(inputx + "\n"))
                return
            else:
                self.telnetClient.write(str.encode(inputx.replace("fuck","funk")+"\n"))
                return
        else:
            self.telnetClient.write(str.encode(inputx + "\n"))

            return inputx

    def auto_attack(self, api: dict = None):
        """
        attack
        """
        api_req = None
        if api is not None:
            api_req = api
        else:
            api_req = self.get_api_dict()
        weapon_attack_speed = common.get_user_info.getUserCond()["attack_speed"]
        if len(api["room"]["enemies"]) != 0:
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

    def print_look(self):
        """
        getting a look at the place the player currently recides
        :return:
        """

        exitNodes = ""
        enemylist = ""
        humanlist = ""
        itemlist = ""
        apireq = self.get_api_dict()
        print(apireq["room"]["name"])

        if "n" in apireq["room"]["exits"]:
            exitNodes += "NORTH "
        if "e" in apireq["room"]["exits"]:
            exitNodes += "EAST "
        if "w" in apireq["room"]["exits"]:
            exitNodes += "WEST "
        if "s" in apireq["room"]["exits"]:
            exitNodes += "SOUTH "

        for i in apireq["room"]["enemies"]:
            enemylist += i

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
