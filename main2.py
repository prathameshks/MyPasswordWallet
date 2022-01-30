from cryptography.fernet import Fernet
import os
import json
import getpass

class Encrypter:
    def __init__(self) -> None:
        pass

    def encrypt(self, key, data):
        manager = Fernet(key)
        e_data = manager.encrypt(data)
        return e_data

    def decrypt(self, key, data):
        manager = Fernet(key)
        d_data = manager.decrypt(data)
        return d_data

    def get_new_key(self):
        key = Fernet.generate_key()
        with open(r"files/key.txt", "w") as file:
            file.write(key.decode('ascii'))
        return key.decode('ascii')

    '''def get_old_key(self):
        if os.path.exists(r'files/oldkey.txt'):
            with open(r"files/oldkey.txt",'r') as oldfile:
                old_data = oldfile.read()
                old_key = old_data.decode('ascii')
            return old_key
        else:
            return False'''

    def get_current_key(self):
        if os.path.exists(r'files/key.txt'):
            with open(r"files/key.txt", 'r') as file:
                key = file.read()
            return key
        else:
            return self.get_new_key()


encrypter = Encrypter()


def strtodict(string):
    dic = json.loads(string)
    return dic


def store_data(data):
    key = bytes(encrypter.get_new_key(), 'ascii')

    with open(r"files/curdata.txt", 'w') as newfile:
        e_data = (encrypter.encrypt(key, json.dumps(
            data).encode('ascii'))).decode('ascii')
        newfile.write(e_data)


def get_current_data():
    key = bytes(encrypter.get_current_key(), 'ascii')
    if os.path.exists(r"files/curdata.txt"):
        with open(r"files/curdata.txt", 'r') as newfile:
            cur_data = newfile.read()
            cur_data = (encrypter.decrypt(
                key, bytes(cur_data, 'ascii'))).decode('ascii')
            return strtodict(cur_data)
    else:
        print("got here")
        return {}


# mydata = {'github':{'username':"sample username",'password':'sample password'},'codechef':{'username':"coed username",'password':'code password'}}
if __name__ == '__main__':
    pass
    # store_data(mydata)
    # print(get_current_data()['github']['username'])


def updatemainpass(dictraw):
    password = getpass.getpass("Enter Profile Password For setting First Time: ")
    dictraw['MPW'] = {'PW': password}
    return dictraw


def startfirst():
    if get_current_data() == {}:
        store_data(updatemainpass({}))


startfirst()
dic2 = get_current_data()
x = list(dic2.keys())
y = x
x.remove('MPW')


def access(p1):
    if p1 == "pks":
        return True
    else:
        return False


def seedata():
    dic2 = get_current_data()
    x = list(dic2.keys())
    y = x
    x.remove('MPW')
    ind = 1
    for k in x:
        print(ind, ": ", k)
        ind += 1
    chs = int(input("Enter Your Choice:"))
    try:
        key = x[chs-1]
        print("Ok")
    except:
        print("Wrong Choice...")
        return None
    maindata = dic2[key]
    datakey = list(maindata.keys())
    try:
        datakey.remove("PW")
    except:
        pass
    for e in datakey:
        print(e, ": ", maindata[e])
    p3 = getpass.getpass("")
    if p3 == dic2['MPW']['PW']:
        try:
            print('PW', ": ", maindata['PW'])
        except:
            print("No Data")

def editdata():
    ind = 1
    y.append("Add New")
    for k in y:
        print(ind, ": ", k)
        ind += 1
    chs = int(input("What You Have To Edit:"))
    try:
        key = y[chs-1]
        print("Ok")
    except:
        print("Wrong Choice...")
        return None
    if key == "Add New":
        an_main = str(input("Enter Main Name:"))
        an_dict = {}
        while True:
            an_1 = str(input("Enter Key Name:"))
            an_2 = str(input("Enter Value Name:"))
            an_dict[an_1] = an_2
            an_ch = str(input("Do you Wish to add more(y/n):"))
            if an_ch not in ["y", "Y", "yes", "Yes", "YES"]:
                break
        dic2[an_main] = an_dict
        store_data(dic2)
        print("Added")

    else:
        addmaindata = dic2[key]
        addind = 1
        z = list(addmaindata.keys())
        z.append("Add New")
        z.append("Remove")
        for l in z:
            print(addind, ": ", l)
            addind += 1
        addchs = int(input("What You Have To Edit:"))
        try:
            addkey = z[addchs-1]
            print("Ok")
        except:
            print("Wrong Choice...")
            return None
        if addkey == "Add New":
            add_key = str(input("Enter New Key:"))
            add_val = str(input("Enter New Value:"))
            dic2[key][add_key] = add_val
            store_data(dic2)
            print('Added')
        elif addkey == "Remove":
            rch = str(input("Do you really want to remove(y/n):"))
            if rch.lower() in ["y", "yes"]:
                dic2.pop(key)
                print("Removed")
            store_data(dic2)
        else:
            change_key = str(input("Enter New Key for "+addkey+":"))
            change_val = str(input("Enter New Valuefor "+addkey+":"))
            dic2[key].pop(addkey)
            dic2[key][change_key] = change_val
            store_data(dic2)
            print("Updated")

canstart = access(getpass.getpass("Enter Password: "))
while True:
    if canstart:
        print("----------Menu----------")
        print("1. See Data")
        print("2. Edit data")
        print("3. Exit")
        ch = int(input("Enter Choice(1/2/3):"))

        if ch == 3:
            break
        p2M = dic2['MPW']['PW']
        p2 = getpass.getpass("Enter Profile Password:")
        if p2 == p2M:
            if ch == 1:
                seedata()
            elif ch == 2:
                editdata()
            else:
                print("Wrong Choice...")
    else:
        canstart=access(getpass.getpass("Enter Password: "))
else:
    print("Thank You!")
