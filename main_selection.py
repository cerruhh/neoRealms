import common.get_user_info
from common.telnetClass import realmsClient
from time import sleep as wait
from colorama import Fore
import storage.art
from multiprocessing import Process
import re
userinfo=common.get_user_info.getUserCond()
host=userinfo["host"]
port=userinfo["port"]



def print_filter(eread:str):
    newre2=''.join(eread.splitlines(keepends=True)[1:])
    return newre2

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

        atk_process=Process(target=client.auto_attack(None))
        atk_process.start()
        atk_process.join()
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
                client.take_all_money(apiparam=apiSend)
                wait(0.126)
                client.send_message(user_command,api=apiSend)
                wait(0.126)
                print(print_filter(bytes.decode(client.telnetClient.read_very_eager())))

            elif user_command[0]=="!":
                cmdx=user_command.split("!")[1]
                client.run_alias(cmdx)

    elif userAsk=="abort":
        exit(0)


if __name__=="__main__":
    main()
    # for i in range(0,10,1):
    #     nproccess=Process(target=main,args=())
    #     nproccess.start()
    #     nproccess.join()