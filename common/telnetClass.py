import string
import telnetlib
import json
import re

import rich
from colorama import Fore
from time import sleep as wait
import common.get_user_info
import threading
from rich import print

writeapitofile=True


class realmsClient:
    def __init__(self,password:str,usrname:str):
        self.telnetClient=telnetlib.Telnet()
        self.password=password
        self.username=usrname
        self.current_room=""

    def connect(self):
        self.telnetClient.open(host="windows93.net", port=8082)
        self.telnetClient.write(str.encode(self.username+"\n"))
        self.telnetClient.write(str.encode(self.password+"\n"))

        return self.telnetClient




    def get_api_dict(self) -> dict:
        while 1:
            self.telnetClient.write(str.encode("api\n"))
            wait(0.01)
            eagerlook=bytes.decode(self.telnetClient.read_very_eager())
            last_line_eager= str.split(eagerlook, "\n")[-1].strip().replace("\n", "")
            ascii_ver=''.join(filter(lambda x: x in string.printable, last_line_eager)).replace("0m","")
            if eagerlook=="":
                continue
            if eagerlook[0]=="[" and eagerlook[-1]!="]":
                ascii_ver+="]"
            if eagerlook[0]=="[" or eagerlook[0]=="{":
                dictver=eval(eagerlook.strip())
                if dictver==[]:
                    continue

                if writeapitofile:
                    with open(file="storage/apistore.json", mode="w", newline=None) as apifile:
                        json.dump(dictver,apifile,indent=3)

                if type(dictver)==list:
                    if len(dictver)==0:
                        continue
                    return dictver[0]
                else:
                    return dictver
            else:
                continue

    def take_all_money(self):
        api=self.get_api_dict()
        room_money=api["room"]["money"]
        if room_money!=0:
            self.telnetClient.write(str.encode("take $"+str(room_money)))
            newapi=self.get_api_dict()
            return room_money

    def send_message(self,inputx:str):
        if inputx=="l" or inputx=="look":
            self.print_look()

        if inputx=="look":
            self.telnetClient.write(str.encode("list\n"))
            print(bytes.decode(self.telnetClient.read_very_eager()))

        if inputx=="n" or inputx=="w" or inputx=="e" or inputx=="s":
            api_req=self.get_api_dict()
            if inputx in api_req["room"]["exits"]:
                self.telnetClient.write(str.encode(inputx+"\n"))
                return True

        if "fuck" in inputx:
            wants_hell=input(Fore.RED+"Are you sure you want to go to hell? (saying fuck will teleport you to hell)? \n (Y/N) > ")
            if wants_hell=="Y":
                self.telnetClient.write(str.encode(inputx))
        else:
            self.telnetClient.write(str.encode(inputx))

        return inputx

    def auto_attack(self):
        api_req=self.get_api_dict()
        weapon_attack_speed=common.get_user_info.getUserCond()["attack_speed"]

        while len(self.get_api_dict()["room"]["enemies"])!=0:
            self.telnetClient.write(str.encode("a\n"))
            wait(weapon_attack_speed)


    def print_latest(self) -> str:
        # print(bytes.decode(self.telnetClient.read_very_eager()))
        print(bytes.decode(self.telnetClient.read_very_eager()))
        return bytes.decode(self.telnetClient.read_very_eager())


    # def get_user_stat_format(self) -> str:
    #     apireq=self.get_api_dict()
    #     return f"""
    #     --------------stats--------------
    #     hp: {apireq['']}
    #     """


    def print_look(self) -> str:
        """
        getting a look at the place the player currently recides
        :return:
        """

        exitNodes=""
        enemylist=""
        humanlist=""
        itemlist=""
        apireq=self.get_api_dict()

        if "n" in apireq["room"]["exits"]:
            exitNodes+="NORTH "
        if "e" in apireq["room"]["exits"]:
            exitNodes+="EAST "
        if "w" in apireq["room"]["exits"]:
            exitNodes+="WEST "
        if "s" in apireq["room"]["exits"]:
            exitNodes+="SOUTH "

        for i in apireq["room"]["enemies"]:
           enemylist+=i

        for i in apireq["room"]["players"]:
            humanlist+=i
        for i in apireq["room"]["items"]:
            itemlist+=i

        exitNodes.strip()
        print(Fore.WHITE+apireq['room']['name'])
        print(Fore.MAGENTA+apireq['room']['description'])
        print(Fore.YELLOW+"exits:"+exitNodes)
        if itemlist!="":
            print(Fore.LIGHTYELLOW_EX+f"You see: {itemlist}")
        if humanlist!="":
            print(Fore.CYAN+f"People: {humanlist}")
        if enemylist!="":
            print(Fore.RED+f"Enemies: {enemylist}")




class Extras:
    def __init__(self):
        pass


    @staticmethod
    def next_level_exp(lv:int):
        return round(100 * (pow(1.4, lv) - 1))
