from cryptography.fernet import Fernet
import os
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

    def get_current_key(self):
        if os.path.exists(r'files/key.txt'):
            with open(r"files/key.txt", 'r') as file:
                key = file.read()
            return key
        else:
            return self.get_new_key()
