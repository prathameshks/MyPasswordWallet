import os
import json
import getpass
from encrypter import Encrypter
import tkinter as tk
from tkinter import messagebox, ttk
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"],default="pbkdf2_sha256",pbkdf2_sha256__default_rounds=30000)
def encryptpass(pw):
    return pwd_context.hash(pw)

def verifypass(pw):
    hashcode = gethash()
    return pwd_context.verify(pw,hashcode)
    

def sethash(pw):
    with open('files/hash.txt','w') as hashfile:
        hashfile.write(encryptpass(pw))
        return True
def gethash():
    with open('files/hash.txt','r') as hashfile:
        hash = hashfile.read()
        return hash


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

def updatemainpass(dictraw,password):
    dictraw['MPW'] = {'PW': password}
    return dictraw

# def showhide():
#     val = pwshohidebtn.cget('text')
#     print(val)
#     if val == 'Hide':
#         pwshohidebtn.config(text='Show')
#         pwentry.config(show='*')
#     else:
#         pwshohidebtn.config(text='Hide')
#         pwentry.config(show=None)
#         pwentry.insert(0,pwentry.get())
#         print("hidden")

def startmainapp():
    main = tk.Frame(win)
    main.grid(row=0,column=0,sticky="NSEW")
    main.tkraise()
    ttk.Label(main,text="Auth Sucess").pack()

def authenticate(pw):
    if verifypass(pw):
        startmainapp()
    else:
        oldstart("Wrong Password",color='red')


def newstart():
    def set():
        global dictraw
        pw1 = pwentry1.get()
        pw2 = pwentry2.get()
        if pw1!=pw2:
            labinfo = ttk.Label(setpass,text='Password Missmatch',justify='center',background='red')
            labinfo.grid(row=3,column=0,columnspan=2,sticky="nsew")
            win.after(3500,lambda: (labinfo.destroy()))
        else:
            if messagebox.askokcancel('Confermation',"Do you really want to set password \nThis operation is ireversiable."):
                sethash(pw1)   
                oldstart("Password created Sucessfully")          
            else:
                newstart()
    setpass = tk.Frame(win)
    setpass.grid(row=0, column=0, sticky='NSEW')
    setpass.tkraise()

    setpass.columnconfigure(0,weight=2)
    setpass.rowconfigure(0,weight=2)
    setpass.rowconfigure(1,weight=1)
    setpass.rowconfigure(2,weight=1)
    # setpass.rowconfigure(3,weight=1)
    setpass.rowconfigure(4,weight=2)
    mainlab = ttk.Label(setpass,text="Create New Password",justify='center',font=("Arial", 15))
    mainlab.grid(row=0,column=0,columnspan=2)

    pwlab1 = ttk.Label(setpass,text='Enter New Password')
    pwlab1.grid(row=1,column=0,sticky="esn")
    pwentry1 = ttk.Entry(setpass,show='*')
    pwentry1.grid(row=1,column=1,sticky="EW",padx=30)
    
    pwlab2 = ttk.Label(setpass,text='Confirm   Password')
    pwlab2.grid(row=2,column=0,sticky="esn")
    pwentry2 = ttk.Entry(setpass,show='*')
    pwentry2.grid(row=2,column=1,sticky="EW",padx=30)
    
    setbtn = ttk.Button(setpass,text="set",command=set)
    setbtn.grid(row=4,column=0,columnspan=2)

    




def resetpass():
    def reset():
        global dictraw
        pw1 = pwentry1.get()
        pw2 = pwentry2.get()
        if pw1!=pw2:
            labinfo = ttk.Label(resetpass,text='Password Missmatch',justify='center',background='red')
            labinfo.grid(row=4,column=0,columnspan=2,sticky="nsew")
            win.after(3500,lambda: (labinfo.destroy()))
        else:
            if messagebox.askokcancel('Confermation',"Do you really want to reset password \nThis operation is ireversiable."):
                sethash(pw1)
                oldstart("Password Reseted Sucessfully")
            else:
                resetpass()
    resetpass = tk.Frame(win)
    resetpass.grid(row=0, column=0, sticky='NSEW')
    resetpass.tkraise()
    resetpass.columnconfigure(0,weight=2)
    resetpass.rowconfigure(1,weight=2)
    resetpass.rowconfigure(2,weight=1)
    resetpass.rowconfigure(3,weight=1)
    # resetpass.rowconfigure(4,weight=1)
    resetpass.rowconfigure(5,weight=2)
    mainlab = ttk.Label(resetpass,text="Reset Password",justify='center',font=("Arial", 15))
    mainlab.grid(row=1,column=0,columnspan=2)
    btnback = ttk.Button(resetpass,text="Back",command=oldstart)
    btnback.grid(row=0,column=1,sticky='e',columnspan=1)
    pwlab1 = ttk.Label(resetpass,text='Enter New Password')
    pwlab1.grid(row=2,column=0,sticky="esn")
    pwentry1 = ttk.Entry(resetpass,show='*')
    pwentry1.grid(row=2,column=1,sticky="EW",padx=30)
    
    pwlab2 = ttk.Label(resetpass,text='Confirm   Password')
    pwlab2.grid(row=3,column=0,sticky="esn")
    pwentry2 = ttk.Entry(resetpass,show='*')
    pwentry2.grid(row=3,column=1,sticky="EW",padx=30)
    
    resetbtn = ttk.Button(resetpass,text="Reset",command=reset)
    resetbtn.grid(row=5,column=0,columnspan=2)

    

def darkstyle(root):
    style = ttk.Style(root)
    root.tk.call('source', 'files/theme/azure dark/azure dark.tcl')
    style.theme_use('azure')
    style.configure("Accentbutton", foreground='white')
    style.configure("Togglebutton", foreground='white')
    return style
style = darkstyle(win)

def oldstart(*args,color='green'):
    if os.path.exists('files/hash.txt'):
        first = True
        def click(*args,first=first):
            if first or pwentry.get()=='Enter Main Password':
                first = False
                pwentry.delete(0, 'end')
                pwentry.config(show='*')

        def leave(*args):
            if pwentry.get()=='':
                pwentry.insert(0, 'Enter Main Password')
                pwentry.config(show=None)

        verification = tk.Frame(win)
        verification.grid(row=0, column=0, sticky='NSEW')

        verification.columnconfigure(0,weight=2)
        verification.rowconfigure(0,weight=2)
        verification.rowconfigure(1,weight=1)
        verification.rowconfigure(2,weight=2)
        verification.rowconfigure(3,weight=2)
        mainlab = ttk.Label(verification,text="Welcome To Password Wallet",justify='center',font=("Arial", 15))
        mainlab.grid(row=0,column=0)

        pwentry = ttk.Entry(verification,show=None)
        pwentry.insert(0, 'Enter Main Password')
        pwentry.grid(row=1,column=0,sticky="EW",padx=30)
        # pwshohidebtn = ttk.Button(verification,text="Show",command=showhide)
        # pwshohidebtn.grid(row=1,column=1,sticky="W")
        pwentry.bind("<Button-1>", click)
        pwentry.bind("<Leave>", leave)

        veribtn = ttk.Button(verification,text="         Authenticate         ",command=lambda:(authenticate(pwentry.get())))
        veribtn.grid(row=2,column=0)

        rsbtn = ttk.Button(verification,text="Reset/Create Password",command=resetpass)
        rsbtn.grid(row=3,column=0,sticky='n')

        messageonveri = ttk.Label(verification,justify='center',foreground=color,font=('arial',10))
        messageonveri.grid(row=4,column=0,sticky='n',pady=10)
        if len(args) == 1:
            messageonveri.config(text=args[0])
            win.after(3500,lambda: (messageonveri.destroy()))
        raise_frame(verification)
    else:
        newstart()

oldstart()


win.mainloop()