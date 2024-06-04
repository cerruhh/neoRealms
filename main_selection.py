import common.get_user_info
from common.telnetClass import realmsClient
from time import sleep as wait
from colorama import Fore
import storage.art
from multiprocessing import Process
host="windows93.net"
port=8082





def login_user():
    """
    create a client to use to interact with Realms93
    :return:
    """
    userinfo=common.get_user_info.getUserCond()
    newRealClient=realmsClient(password=userinfo["password"],usrname=userinfo["username"])
    return newRealClient



def main():
    """
    main function
    :return:
    """
    print(Fore.YELLOW+storage.art.welcomeart)
    while True:
        userAsk = input("what do you want to do? (gui,cli,abort)?\n > ").lower()
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
                line = client.telnetClient.read_until(str.encode("\n"),timeout=1)
                print(bytes.decode(line).replace("93 Realms", "neoRealms"))
                client.send_message(user_command)
                client.take_all_money()
                client.auto_attack()
                print(bytes.decode(client.telnetClient.read_very_eager()).replace("93 Realms","neoRealms"))
            elif user_command[0]=="!":
                line = client.telnetClient.read_until(b"\n\r",timeout=1)
                print(bytes.decode(line))
                cmdx=user_command.split("!")[1]
                client.run_alias(cmdx)
                print(bytes.decode(client.telnetClient.read_some()))
    elif userAsk=="abort":
        exit(0)


if __name__=="__main__":
    main()