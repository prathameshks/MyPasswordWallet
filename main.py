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

    def get_key(self):
        if os.path.exists(r'files/key.txt'):
            with open(r"files/key.txt","r") as file:
                filedata = file.read()
            with open(r"files/oldkey.txt",'w') as oldfile:
                oldfile.write(filedata)    
            return filedata
        else:
            key = Fernet.generate_key()
            with open(r"files/key.txt","w") as file:
                file.write(key)
            return key

encrypter = Encrypter()

print(encrypter.get_key())