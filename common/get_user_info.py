import json
def getUserCond():
    with open(file="common/accountdata.json",mode="r") as accountData:
        zix=json.load(accountData)
        return zix["info"]

