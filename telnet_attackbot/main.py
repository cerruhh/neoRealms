import telnetlib
from time import sleep as wait
import colorama
from common.get_user_info import getUserCond
cond=getUserCond()

#user_cond=getUserCond()
host="windows93.net"
port=8082
runcommand="run 8w1n3w2n\n"
isAlreadyThere=False
waitspeed=cond["attack_speed"]

# telnetClient=telnetlib.Telnet()
# telnetClient.open(host=host,port=port)
# wait(0.3)
# print("logging in")
# telnetClient.write(str.encode(cond["info"]["username"]+'\n'))#username
# telnetClient.write(str.encode(cond["info"]["password"]+"\n"))
# print("logged in, read until loaded")
# wait(1)
# #telnetClient.read_until(str.encode(f"{cond['info']['username']} has entered the realm."))
# print("logged in, wait for travel time")
# secondsCount=0



# if not isAlreadyThere:
#     telnetClient.write(str.encode(runcommand))
#     wait(10)


def start_attackuser(cond,telentclient):
    secondsCount=0
    while True:
        #telnetClient.write(str.encode("take $506\n"))
        wait(waitspeed)
        telentclient.write(str.encode("a\n"))
        excra = bytes.decode(telentclient.read_very_eager())
        secondsCount+=1
        print(excra)
        if '$' in excra:
            newExa="$"+str(excra[excra.find("$").__index__()+1])+str(excra[excra.find("$").__index__()+2])
            telentclient.write(str.encode("take "+newExa))
            telentclient.write(str.encode("inv\n"))
            print(colorama.Fore.YELLOW+f"bot up for {str(secondsCount)} seconds")
