import os
import json
import sys
from encrypter import Encrypter
import tkinter as tk
from tkinter import PhotoImage, messagebox, ttk
from passlib.context import CryptContext
from PIL import ImageTk ,Image
from files import drive_api

# for encrypting and storing password
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
    drive_api.set_data('key.txt',key.decode('ascii'))
    e_data = (encrypter.encrypt(key, json.dumps(data).encode('ascii'))).decode('ascii')
    drive_api.set_data('curdata.txt',e_data)

def get_current_data():
    key = bytes(encrypter.get_current_key(), 'ascii')
    if drive_api.if_exists('curdata.txt')[0]:
        cur_data = drive_api.get_data('curdata.txt')
        cur_data = (encrypter.decrypt(
            key, bytes(cur_data, 'ascii'))).decode('ascii')
        return strtodict(cur_data)
    else:
        print("got here")
        return {}

def restart_app():
    os.startfile(__file__)
    print('restarted')
    sys.exit()

loading_frame = tk.Frame(win)
loading_frame.grid(row=0,column=0,sticky="NSEW")

loading_frame.rowconfigure(0, weight=2)
loading_frame.columnconfigure(0, weight=2)
ttk.Label(loading_frame,text="Loading...").grid(row=0,column=0,sticky="NSEW")


# main app after main password veri sucess
def startmainapp():
    main = tk.Frame(win)
    main.grid(row=0,column=0,sticky="NSEW")
    main.tkraise()
    ttk.Label(main,text="Auth Sucess").pack()
    print(get_current_data())


def authenticate(pw):
    if verifypass(pw):
        loading_frame.tkraise()
        # startmainapp()
    else:
        oldstart("Wrong Password",color='red')


# for starting new or first time ie show create pass window
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

def reset_data():
    if os.path.exists('files/token_drive_v3.pickle'):
        os.remove('files/token_drive_v3.pickle')
        print('deleted old token')
    else:
        print('no data exists')



# reset passowrd main
# still find way to make authenticate for password change
def reset_password_fun():
    def reset():
        global dictraw
        pw1 = pwentry1.get()
        pw2 = pwentry2.get()
        if pw1!=pw2:
            labinfo = ttk.Label(reset_password,text='Password Missmatch',justify='center',background='red')
            labinfo.grid(row=4,column=0,columnspan=2,sticky="nsew")
            win.after(3500,lambda: (labinfo.destroy()))
        else:
            if messagebox.askokcancel('Confermation',"This operation is ireversiable And need to reauthenticate with Google\nDo you really want to reset app?",):
                sethash(pw1)
                reset_data()
                messagebox.showinfo('Password Reset',"Password Reseted Sucessfully.\nWe need to restart the Application.")
                restart_app()
            else:
                reset_password_fun()
    reset_password = tk.Frame(win)
    reset_password.grid(row=0, column=0, sticky='NSEW')
    reset_password.tkraise()
    reset_password.columnconfigure(0,weight=2)
    reset_password.rowconfigure(1,weight=2)
    reset_password.rowconfigure(2,weight=1)
    reset_password.rowconfigure(3,weight=1)
    # reset_password.rowconfigure(4,weight=1)
    reset_password.rowconfigure(5,weight=2)
    mainlab = ttk.Label(reset_password,text="Reset Password",justify='center',font=("Arial", 15))
    mainlab.grid(row=1,column=0,columnspan=2)
    btnback = ttk.Button(reset_password,text="Back",command=oldstart)
    btnback.grid(row=0,column=1,sticky='e',columnspan=1)
    pwlab1 = ttk.Label(reset_password,text='Enter New Password')
    pwlab1.grid(row=2,column=0,sticky="esn")
    pwentry1 = ttk.Entry(reset_password,show='*')
    pwentry1.grid(row=2,column=1,sticky="EW",padx=30)
    
    pwlab2 = ttk.Label(reset_password,text='Confirm   Password')
    pwlab2.grid(row=3,column=0,sticky="esn")
    pwentry2 = ttk.Entry(reset_password,show='*')
    pwentry2.grid(row=3,column=1,sticky="EW",padx=30)
    
    resetbtn = ttk.Button(reset_password,text="Reset",command=reset)
    resetbtn.grid(row=5,column=0,columnspan=2)

    

def darkstyle(root):
    style = ttk.Style(root)
    root.tk.call('source', 'files/theme/azure dark/azure dark.tcl')
    style.theme_use('azure')
    style.configure("Accentbutton", foreground='white')
    style.configure("Togglebutton", foreground='white')
    return style
# style = darkstyle(win)

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
        verification.columnconfigure(1,weight=2)
        verification.rowconfigure(0,weight=2)
        verification.rowconfigure(1,weight=1)
        verification.rowconfigure(2,weight=2)
        verification.rowconfigure(3,weight=1)
        mainlab = ttk.Label(verification,text="Welcome To Password Wallet",justify='center',font=("Arial", 15))
        mainlab.grid(row=0,column=0,columnspan=2)

        pwentry = ttk.Entry(verification,show=None)
        pwentry.insert(0, 'Enter Main Password')
        pwentry.grid(row=1,column=0,sticky="EW",padx=30,columnspan=2)
        # pwshohidebtn = ttk.Button(verification,text="Show",command=showhide)
        # pwshohidebtn.grid(row=1,column=1,sticky="W")
        pwentry.bind("<Button-1>", click)
        pwentry.bind("<Leave>", leave)

        forgotpwbtn = ttk.Button(verification,text="Forgot Password",command=reset_password_fun)
        forgotpwbtn.grid(row=2,column=0)
        
        messageonveri = ttk.Label(verification,justify='center',foreground=color,font=('arial',10))
        messageonveri.grid(row=4,column=0,sticky='n',pady=10,columnspan=2)
        
        veribtn = ttk.Button(verification,text="Authenticate",command=lambda:(authenticate(pwentry.get())))
        veribtn.grid(row=2,column=1)

        # rsbtn = ttk.Button(verification,text="Reset App")
        # rsbtn.grid(row=3,column=0,sticky='n',columnspan=2)
        
        if len(args) == 1:
            messageonveri.config(text=args[0])
            win.after(3500,lambda: (messageonveri.destroy()))
        raise_frame(verification)
    else:
        newstart()

oldstart()

def set_theme(thm):
    with open("files/theme.txt",'w') as thm_file:
        thm_file.write(thm)

def get_theme():
    if os.path.exists("files/theme.txt"):
        with open("files/theme.txt",'r') as thm_file:
            thm = thm_file.read()
            if thm in ['light','dark']:
                return thm
            else:
                set_theme('light')
                return 'light'
    else:
        set_theme('light')
        return 'light'


bottom_bar = tk.Frame(win)
bottom_bar.grid(row=1,column=0,sticky='nsew')
bottom_bar.tkraise()

# Set the initial theme
win.tk.call("source", "files/theme/sunvallydark-white/sun-valley.tcl")
win.tk.call("set_theme", get_theme())

# images
light_image = ImageTk.PhotoImage((Image.open('files/light.png')).resize((20, 20), Image.ANTIALIAS))
dark_image = ImageTk.PhotoImage((Image.open('files/dark.png')).resize((20, 20), Image.ANTIALIAS))

def change_theme():
    # NOTE: The theme's real name is sun-valley-<mode>
    if win.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
        # Set light theme
        win.tk.call("set_theme", "light")
        set_theme('light')
        button_chng_thm.config(image=dark_image)
    else:
        # Set dark theme
        win.tk.call("set_theme", "dark")
        set_theme('dark')
        button_chng_thm.config(image=light_image) 

# Remember, you have to use ttk widgets
button_chng_thm = ttk.Button(bottom_bar, command=change_theme,compound='center')
button_chng_thm.pack(side='left')
if get_theme()=='light':
    button_chng_thm.config(image = dark_image)
else:
    button_chng_thm.config(image=light_image) 

# store_data({'main':{'pw':'pks','us':'pksuser'},'2':{'user':'123'}})

win.mainloop()