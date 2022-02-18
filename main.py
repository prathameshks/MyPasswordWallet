import os
import json
import sys
from time import sleep
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
        print("No data in drive")
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

#windows for saved data


# making new object with get ethod to continue in for loop
class similar_entry:
    def __init__(self,name) -> None:
        self.name = name
    def get(self):
        return self.name
#window to addd new data
def add_new_data():
    add_data_frame = tk.Frame()
    add_data_frame.grid(row=0,column=0,sticky="NSEW") 
    add_data_frame.tkraise()
    padding_x,padding_y=10,(5,5)
    labmain = ttk.Label(add_data_frame,text='Enter Details Below',justify='center',font=("Arial", 15))
    labmain.grid(row=0,column=0,columnspan=3,padx=padding_x,pady=padding_y)
    lab1 = ttk.Label(add_data_frame,text='Name of website or App')
    lab1.grid(row=1,column=0,padx=padding_x,pady=padding_y)
    
    # adding weight
    add_data_frame.columnconfigure(0,weight=2)
    add_data_frame.columnconfigure(1,weight=2)

    add_data_frame.rowconfigure(0,weight=3)
    add_data_frame.rowconfigure(1,weight=2)
    
    name_entry = ttk.Entry(add_data_frame)
    name_entry.grid(row=1,column=1,padx=padding_x,pady=padding_y)
    datanames=[]
    datavalue=[]

    #data addition function to store to drive
    def add_data():
        for index in range(len(datavalue)):
            data_n,data_e = datanames[index],datavalue[index]
            print(data_n.get().title(),data_e.get())

    global r
    r = 2
    datafilds = ['Username','Email ID','Mobile Number','Password',"Add Other"]
    show_other_name = tk.StringVar()
    
    def selected_something(*args):
        global r
        name = show_other_name.get()
        if name=='Add Other':
            data_name = ttk.Entry(add_data_frame)
            data_name.grid(row=r,column=0,padx=padding_x,pady=padding_y)
            data_entry = ttk.Entry(add_data_frame)
            data_entry.grid(row=r,column=1,padx=padding_x,pady=padding_y)
            
            datanames.append(data_name)
            datavalue.append(data_entry)
            r+=1
        elif name=="Password":
            data_name = ttk.Label(add_data_frame,text=name)
            data_name.grid(row=r,column=0,padx=padding_x,pady=padding_y)
            data_name_entry = similar_entry(name)
            data_entry = ttk.Entry(add_data_frame,show='*')
            data_entry.grid(row=r,column=1,padx=padding_x,pady=padding_y)
            datanames.append(data_name_entry)
            datavalue.append(data_entry)
            datafilds.remove(name)
            r+=1
        else:
            data_name = ttk.Label(add_data_frame,text=name)
            data_name.grid(row=r,column=0,padx=padding_x,pady=padding_y)
            data_name_entry = similar_entry(name)
            data_entry = ttk.Entry(add_data_frame)
            data_entry.grid(row=r,column=1,padx=padding_x,pady=padding_y)
            datanames.append(data_name_entry)
            datavalue.append(data_entry)
            datafilds.remove(name)
            r+=1
        add_data_frame.rowconfigure(r-1,weight=2)
        add_data_frame.rowconfigure(r,weight=2)
        add_data_frame.rowconfigure(r+1,weight=2)
        
        show_other.grid(row=r,column=0,padx=padding_x,pady=padding_y)
        submit_new_data.grid(row=r+1,column=1,padx=padding_x,pady=padding_y)
        show_other['values'] = datafilds

    show_other = ttk.Combobox(add_data_frame,values=datafilds,textvariable=show_other_name,state='readonly')
    show_other.grid(row=r,column=0,padx=padding_x,pady=padding_y)
    show_other.bind('<<ComboboxSelected>>', selected_something)

    submit_new_data = ttk.Button(add_data_frame,text="Save data",command=add_data)
    submit_new_data.grid(row=r+1,column=1,padx=padding_x,pady=padding_y)

# main app after main password veri sucess
def startmainapp():
    main = tk.Frame(win)
    main.grid(row=0,column=0,sticky="NSEW") 
    main.tkraise()

    # defining weights
    main.rowconfigure(0,weight=3)
    main.rowconfigure(1,weight=1)
    main.rowconfigure(2,weight=2)
    main.rowconfigure(3,weight=2)

    main.columnconfigure(0,weight=2)
    # label for main window
    main_label = ttk.Label(main,text="Welcome to\nMy Password Wallet",justify='center',font=("Arial", 20))
    main_label.grid(row=0,column=0)

    # messsage to display
    main_msz = ttk.Label(main,text="Login Sucessful",justify='center',font=("", 10),foreground='green')
    main_msz.grid(row=1,column=0)
    win.after(5000,lambda : (main_msz.destroy()))
    #define buttons for old data view edit delete
    btnold = ttk.Button(main,text="Get Saved Password")
    btnold.grid(row=2,column=0)

    #to add new data
    btnnew = ttk.Button(main,text="Save New Password",command=add_new_data)
    btnnew.grid(row=3,column=0)

    # ttk.Label(main,text="Auth Sucess").pack()


def authenticate(pw):
    if verifypass(pw):
        raise_frame(loading_frame)
        startmainapp()
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
            if messagebox.askokcancel('Confermation',"Do you really want to set this password \nThis operation is ireversiable."):
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

if __name__=='__main__':
    # oldstart()
    startmainapp()

win.mainloop()