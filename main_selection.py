import common.get_user_info
from common.telnetClass import realmsClient
host="windows93.net"
port=8082





def login_user():
    userinfo=common.get_user_info.getUserCond()
    newRealClient=realmsClient(password=userinfo["password"],usrname=userinfo["username"])
    return newRealClient



def main():
    userAsk = input("what do you want to do? (attack, getstats, client, abort)?\n > ")
    if userAsk=="client":
        client=login_user()
        connection_rec=client.connect()
        # autoattack_class=ThreadClass(fdownload=client.auto_attack())
        # autoattack_class.start()
        # autoattack_class.join()

        while True:
            user_command=input(" > ")
            if user_command=="":
                continue

            if user_command[0]!="!":
                client.send_message(user_command)
                client.take_all_money()
                client.auto_attack()
    elif userAsk=="abort":
        exit(0)
    elif userAsk=="getstats":
        client=login_user()
        connection_rec=client.connect()



if __name__=="__main__":
    main()