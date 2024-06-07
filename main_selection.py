import common.get_user_info
from common.telnetClass import realmsClient,Extras
from time import sleep as wait
from colorama import Fore
import storage.art
from multiprocessing import Process
from threading import Thread
import concurrent.futures

import re
userinfo=common.get_user_info.getUserCond()
host=userinfo["host"]
port=userinfo["port"]



def print_filter(eread:str):
    # Define the regex pattern to exclude lines starting with [ or { and ending with ] or }
    pattern = r"^(?![{\[]).*?(?<![}\]])$"

    # Find all matching lines
    matching_lines = re.findall(pattern, eread, flags=re.MULTILINE)

    # Join the matching lines into a single string
    filtered_text = "\n".join(matching_lines)

    return filtered_text
    # .join(eread.split("\n")[1:])


def print_status(status:str):
    print("\u001B[s", end="")  # Save current cursor position
    print("\u001B[A", end="")  # Move cursor up one line
    print("\u001B[999D", end="")  # Move cursor to beginning of line
    print("\u001B[S", end="")  # Scroll up/pan window down 1 line
    print("\u001B[L", end="")  # Insert new line
    print(status, end="")  # Print output status msg
    print("\u001B[u", end="")  # Jump back to saved cursor position


def proc_read(cl):
    wait(1)
    oread=print_filter(bytes.decode(cl.telnetClient.read_very_eager(),encoding="latin-1"))
    while True:
        newread=print_filter(bytes.decode(cl.telnetClient.read_very_eager()))
        if newread!=oread and (newread!="" or newread!="\n"):
            print_status(newread.strip())
            oread=newread
        wait(0.5)






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
        if userAsk=="gui" or userAsk=="g" or userAsk=="c" or userAsk=="cli" or userAsk=="a" or userAsk=="abort" or userAsk=="about":
            break

    if userAsk=="cli" or userAsk=="c":
        client=login_user()
        connection_rec=client.connect()
        wait(0.2)
        lastcommand=""

        atk_process=Thread(target=client.auto_attack)
        atk_process.start()
        client.print_look()

        lookproc=Thread(target=proc_read,args=[client])
        lookproc.start()

#       print(repr(client.telnetClient.read_all()))
        while True:
            wait(0.2)
            user_command=input("\n")
            if user_command=="":
                if lastcommand!="":
                    ism=client.send_message(lastcommand.strip())
                    wait(.2)
                else:
                    continue
            else:
                lastcommand=user_command

                if user_command[0]!="!":
                    apiSend=client.get_api_dict()
                    if apiSend is not None:
                        client.take_all_money(apiparam=apiSend)
                        wait(0.126)
                        client.send_message(user_command,api=apiSend,isrecall=False)
                elif user_command[0]=="!":
                    cmdx=user_command.split("!")[1]
                    if cmdx=="aaf":
                        infiProcess=Process(target=client.infiniatk())
                        infiProcess.start()
                        continue
                    else:
                        client.run_alias(cmdx)
    elif userAsk=="about":
        print(Fore.YELLOW+storage.art.welcomeart)
        print("""
        Welcome to neorealms,
        a custom realms client created by cerruhh designed to make the realms93 experience better.
        
        2024-3000
        """)
        exit(2015)

    elif userAsk=="abort":
        exit(0)


if __name__=="__main__":
    main()