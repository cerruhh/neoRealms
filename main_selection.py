import common.get_user_info
from common.telnetClass import realmsClient
from time import sleep as wait
from colorama import Fore
import storage.art
from multiprocessing import Process
userinfo=common.get_user_info.getUserCond()
host=userinfo["host"]
port=userinfo["port"]





def login_user():
    """
    create a client to use to interact with Realms93
    :return:
    """
    if userinfo["debug_level"]!=0:
        debuglevel=userinfo["debug_level"]
        newRealClient=realmsClient(password=userinfo["password"],usrname=userinfo["username"],dbglv=debuglevel)
        return newRealClient
    else:
        debuglevel = userinfo["debug_level"]
        newRealClient = realmsClient(password=userinfo["password"], usrname=userinfo["username"], dbglv=debuglevel)
        return newRealClient


def main():
    """
    main function
    :return:
    """
    print(Fore.YELLOW+storage.art.welcomeart)
    while True:
        userAsk = input(Fore.RESET+"what do you want to do? (gui,cli,abort)?\n > ").lower()
        if userAsk=="gui" or userAsk=="g" or userAsk=="c" or userAsk=="cli" or userAsk=="a" or userAsk=="abort":
            break

    if userAsk=="cli" or userAsk=="c":
        client=login_user()
        connection_rec=client.connect()
        # autoattack_class=ThreadClass(fdownload=client.auto_attack())
        # autoattack_class.start()
        # autoattack_class.join()
        wait(0.2)
        lastcommand=""
        while True:
            wait(0.2)
            user_command=input(" > ")
            if user_command=="":
                if lastcommand!="":
                    client.send_message(lastcommand)
                continue

            lastcommand=user_command

            if user_command[0]!="!":
                apiSend=client.get_api_dict()
                client.send_message(user_command,api=apiSend)
                client.take_all_money(apiparam=apiSend)
                client.auto_attack(api=apiSend)
            elif user_command[0]=="!":
                cmdx=user_command.split("!")[1]
                client.run_alias(cmdx)

    elif userAsk=="abort":
        exit(0)


if __name__=="__main__":
    main()