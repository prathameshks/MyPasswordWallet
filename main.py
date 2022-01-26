from cryptography.fernet import Fernet
import os

class Encrypter:
    def encrypt(self,key,data):
        manager = Fernet(key) 
        e_data = manager.encrypt(data)
        return e_data
    
    def decrypt(self,key,data):
        manager = Fernet(key) 
        d_data = manager.decrypt(data)
        return d_data

    def get_new_key(self):
        if os.path.exists(r'files/key.txt'):
            newkey = Fernet.generate_key()
            with  open(r"files/key.txt","r") as file1:
                filedata = file1.read()
            with open(r"files/oldkey.txt",'w') as oldfile:
                oldfile.write(filedata) 
            with  open(r"files/key.txt","w") as file1:
                filedata = file1.write(newkey.decode('ascii'))
            return newkey
        else:
            key = Fernet.generate_key()
            with open(r"files/key.txt","w") as file:
                file.write(key.decode('ascii'))
            return key
    

encrypter = Encrypter()

print(encrypter.get_new_key())