from cryptography.fernet import Fernet
import os
from files import drive_api

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
        drive_api.set_data('key.txt',key.decode('ascii'))
        print('new key generated')
        return key.decode('ascii')

    def get_current_key(self):
        if drive_api.if_exists('key.txt')[0]:
            print('key found')
            key = drive_api.get_data('key.txt')
            return key
        else:
            print('key not found')
            return self.get_new_key()
