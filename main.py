from ast import keyword
from errno import EADDRNOTAVAIL
import os
import encryption
encrypter = encryption.Encrypter()

def store_data(data):
    key = bytes(encrypter.get_new_key(),'ascii')
    print(key)
    if os.path.exists(r"files/curdata.txt"):
        with open(r"files/curdata.txt",'r') as curfile:
            data = curfile.read()
            # old_content = encrypter.decrypt(key,data).decode('ascii')
        with open(r"files/olddata.txt",'w') as oldfile:
            oldfile.write(data)
    with open(r"files/curdata.txt",'w') as newfile:
        data_to_encrypt = bytes(str(data),'ascii')
        print(data_to_encrypt)
        e_data = (encrypter.encrypt(key,data_to_encrypt)).decode('ascii')
        print(e_data)
        newfile.write(e_data)

def get_current_data():
    key = bytes(encrypter.get_current_key(),'ascii')
    if os.path.exists(r"files/curdata.txt"):
        with open(r"files/curdata.txt",'r') as newfile:
            cur_data = newfile.read()
            cur_data = (encrypter.decrypt(key,bytes(cur_data,'ascii'))).decode('ascii')
            cur_dict = {}
            exec("cur_dict = "+str(cur_data))
            return cur_dict
    else:
        return {}

mydata = {'github':{'username':"sample username",'password':'sample password'},'codechef':{'username':"coed username",'password':'code password'}}
if __name__ == '__main__':
    # store_data(mydata)
    print(get_current_data())