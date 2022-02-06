import os
import json
import getpass
from encrypter import Encrypter
import tkinter as tk
from tkinter import ttk
from passlib.context import CryptContext
from ttkthemes import ThemedStyle

pwd_context = CryptContext(schemes=["pbkdf2_sha256"],default="pbkdf2_sha256",pbkdf2_sha256__default_rounds=30000)
def encryptpass(pw):
    return pwd_context.hash(pw)

def verifypass(pw,hashcode):
    return pwd_context.verify(pw,hashcode)

win = tk.Tk()
win.geometry('300x300')
win.title('My Password Wallet')
win.iconbitmap(r'files/icon.ico')
win.minsize(300,300)
def raise_frame(frame):
    frame.tkraise()

win.rowconfigure(0,weight=1)
win.columnconfigure(0,weight=1)




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


def updatemainpass(dictraw):
    password = getpass.getpass("Enter Profile Password For setting First Time: ")
    dictraw['MPW'] = {'PW': password}
    return dictraw


def startfirst():
    if get_current_data() == {}:
        store_data(updatemainpass({}))


startfirst()

first = True
def click(*args):
    global first
    if first or pwentry.get()=='Enter Main Password':
        first = False
        pwentry.delete(0, 'end')

def leave(*args):
    if pwentry.get()=='':
        pwentry.insert(0, 'Enter Main Password')

def authenticate():
    menu = tk.Frame(win)
    menu.tkraise()
    menu.grid(row=0,column=0,sticky="NSEW")
        
    menu_op1 = tk.Button(menu,text="View Saved")
    menu_op1.grid(row=0,column=0)
    return None


def darkstyle(root):
    ''' Return a dark style to the window'''
    
    style = ttk.Style(root)
    root.tk.call('source', 'files/theme/azure dark/azure dark.tcl')
    style.theme_use('azure')
    style.configure("Accentbutton", foreground='white')
    style.configure("Togglebutton", foreground='white')
    return style
style = darkstyle(win)

verification = tk.Frame(win)
# style = ThemedStyle(verification)
# style.set_theme("equilux")
verification.grid(row=0, column=0, sticky='NSEW')

verification.columnconfigure(0,weight=2)
# verification.columnconfigure(1,weight=1)
verification.rowconfigure(0,weight=2)
verification.rowconfigure(1,weight=1)
verification.rowconfigure(2,weight=2)
mainlab = ttk.Label(verification,text="Welcome To Password Wallet",justify='center',font=("Arial", 15))
mainlab.grid(row=0,column=0)

pwentry = ttk.Entry(verification)
pwentry.insert(0, 'Enter Main Password')
pwentry.grid(row=1,column=0,sticky="EW",padx=30)
pwentry.bind("<Button-1>", click)
pwentry.bind("<Leave>", leave)

veribtn = ttk.Button(verification,text="Authenticate",command=authenticate)
veribtn.grid(row=2,column=0)

raise_frame(verification)





win.mainloop()