import setup

if not setup.needs_setup():
    setup.setup()
    exit(0)
import common.get_user_info
# import curses
# from curses import wrapper
from common.telnetClass import realmsClient
from time import sleep as wait
from colorama import Fore
import storage.art
from multiprocessing import Process
from threading import Thread
import common.shop_lists
import os

import re

userinfo = common.get_user_info.getUserCond()
host = userinfo["host"]
port = userinfo["port"]

is_nt = os.name == "nt"
list_start_commands = ["c", "cli", "a", "abort", "about"]


# Is Windows (opens README.md in notepad if so)


def print_filter(eread: str):
    # Define the regex pattern to exclude lines starting curly braces and brackets
    pattern = r"^(?![{\[]).*?(?<![}\]])$"

    # Find all matching lines
    matching_lines = re.findall(pattern, eread, flags=re.MULTILINE)

    # Join the matching lines into a single string
    filtered_text = "\n".join(matching_lines)

    return filtered_text
    # .join(eread.split("\n")[1:])


def print_status(status: str):
    print("\u001B[s", end="")  # Save current cursor position
    print("\u001B[A", end="")  # Move cursor up one line
    print("\u001B[999D", end="")  # Move cursor to beginning of line
    print("\u001B[S", end="")  # Scroll up/pan window down 1 line
    print("\u001B[L", end="")  # Insert new line
    print(status, end="")  # Print output status msg
    print("\u001B[u", end="")  # Jump back to saved cursor position


def remove_api(stringx: str):
    """
    removes { from string
    :param stringx:
    :return:
    """
    newstring = ""
    for i in stringx.splitlines():
        if i != "" and i[0] != "{":
            newstring += i + "\n"

    return newstring


def proc_read(cl):
    wait(1)
    oread = remove_api(print_filter(bytes.decode(cl.telnetClient.read_very_eager(), encoding="utf-8")))
    while True:
        if cl.exited:
            exit(0)
        newread = print_filter(bytes.decode(cl.telnetClient.read_very_eager()))
        read_convert = remove_api(newread)
        if read_convert != oread and (read_convert != "" or read_convert != "\n"):
            print_status(read_convert.strip())
            oread = read_convert
        wait(0.5)


def login_user(username: str = userinfo["username"], password: str = userinfo["password"]):
    """
    creates a login_user realmsclient
    :param username:
    :param password:
    :return:
    """
    debuglevel = userinfo["debug_level"]
    newRealClient = realmsClient(password=password, usrname=username, dbglv=debuglevel)
    return newRealClient


def main():
    """
    main function
    :return:
    """

    global client
    if userinfo["welcome_art"]:
        if userinfo["small_welcome_art"]:
            print(Fore.YELLOW + storage.art.smallwelcomeart)
        else:
            print(Fore.YELLOW + storage.art.welcomeart)
    if userinfo["debug_level"] > 0:
        print(Fore.RESET + "Warning! User running neorealms with debug level enabled!")

    while True:
        userAsk = input(Fore.RESET + "what do you want to do? (cli (-d for select account),abort, about)?\n > ").lower()
        userSplit = userAsk.split(" ")[0]
        if userSplit in list_start_commands:
            break

    if userSplit == "cli" or userSplit == "c":
        sp_param_len = len(userAsk.split(" ")) == 2
        sp_param = ""
        if sp_param_len:
            sp_param = userAsk.split(" ")[1]
        print(sp_param)
        #       len_users = len(userinfo["accounts"])
        if sp_param == "-d":
            # If there are more than 1 user, select user.
            print(Fore.GREEN + "Multiple Accounts Detected! Please select an account ")
            for i in userinfo["accounts"]:
                print(Fore.GREEN + "extra > " + i['username'])
            print(Fore.GREEN + "default > " + userinfo["username"])

            while True:
                user_selected = input(
                    Fore.YELLOW + "Please Select User by username, or if you want the default account, type 'default'\n > ")
                isfound=False
                if user_selected == "default":
                    client = login_user()
                    break
                for i in userinfo["accounts"]:
                    if str(i["username"]) == user_selected:
                        print(i["username"])
                        client = login_user(username=i["username"], password=i["password"])
                        isfound = True
                        break
                if isfound:
                    break
        else:
            client = login_user()

        client.connect()
        wait(userinfo["delay"])
        lastcommand = ""

        # atk_process = Thread(target=client.auto_attack)
        # atk_process.start()
        client.print_look()

        lookproc = Thread(target=proc_read, args=[client])
        lookproc.start()

        #       print(repr(client.telnetClient.read_all()))
        autocollect = True
        while True:
            # Main Loop
            user_command = input(Fore.RESET + "\n")
            if user_command == "":
                if lastcommand != "":
                    client.send_message(lastcommand.strip())
                    print(Fore.RESET + f"Sent command: {lastcommand.strip()}")
                    wait(userinfo["delay"])
                else:
                    continue
            else:
                lastcommand = user_command

                if user_command[0] != "!":
                    # Runas normal command
                    apiSend = client.get_api_dict()
                    # If the api command worked
                    if apiSend is not None:
                        client.send_message(user_command, api=apiSend, isrecall=False)
                        # If autocollect is enabled, run this
                        if autocollect:
                            # 200ms delay
                            wait(userinfo["delay"])
                            client.take_all_money(apiparam=apiSend)
                        continue
                elif user_command[0] == "!":
                    # Run as alias \!
                    if user_command == "!":
                        for i in userinfo["aliases"]:
                            print(Fore.YELLOW + i.split("|")[0])
                    cmdx = user_command.split("!")[1]
                    if cmdx == "aaf":
                        infiProcess = Process(target=client.infiniatk())
                        infiProcess.start()
                        continue
                    elif cmdx == "autocollect":
                        autocollect = not autocollect
                        print(f"Autocollect set to: {str(autocollect)}")
                        continue
                    elif cmdx == "autocolst":
                        print(f"Autocollect status: {str(autocollect)}")
                        continue
                    else:
                        client.run_alias(cmdx)

            wait(userinfo["delay"])
    elif userAsk == "about":
        if userinfo["small_welcome_art"]:
            print(Fore.RED + storage.art.smallwelcomeart)
        else:
            print(Fore.RED + storage.art.welcomeart)

        print(Fore.RESET+"Neo Realms is a project by cerruhh. Neorealms aims to make playing realms93 more modular, and giving the player nessecary abilites, and quality of life improvements.")
        print("Neorealms is licensed under the GPL v3.0 license. You can find the license under the LICENSE file.")
        exit(2015)

    elif userAsk == "abort":
        exit(0)
    # elif userAsk == "bot":
    #     client = login_user()
    #     while 1:
    #         wait(userinfo["attack_speed"])
    #         client.send_message("a")
    #


if __name__ == "__main__":
    main()
