import os
import json
import sys
from encrypter import Encrypter
import tkinter as tk
from tkinter import PhotoImage, messagebox, ttk
from passlib.context import CryptContext
from PIL import ImageTk, Image
from files import drive_api

# for encrypting and storing password
pwd_context = CryptContext(schemes=[
                           "pbkdf2_sha256"], default="pbkdf2_sha256", pbkdf2_sha256__default_rounds=30000)


def encryptpass(pw):
    return pwd_context.hash(pw)


def verifypass(pw):
    hashcode = gethash()
    return pwd_context.verify(pw, hashcode)


def sethash(pw):
    with open('files/hash.txt', 'w') as hashfile:
        hashfile.write(encryptpass(pw))
        return True


def gethash():
    with open('files/hash.txt', 'r') as hashfile:
        hash = hashfile.read()
        return hash


win = tk.Tk()
win.geometry('500x600+200+50')
win.title('My Password Wallet')
win.iconbitmap(r'files/icon.ico')
win.minsize(300, 300)


# creating tooltip object 
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text):
        self.waittime = 300     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left', relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

edit_image = ImageTk.PhotoImage(
    (Image.open('files/edit.png')).resize((20, 20), Image.ANTIALIAS))
delete_image = ImageTk.PhotoImage(
    (Image.open('files/delete.png')).resize((20, 20), Image.ANTIALIAS))
def raise_frame(frame):
    frame.tkraise()


win.rowconfigure(0, weight=1)
win.columnconfigure(0, weight=1)


encrypter = Encrypter()


def strtodict(string):
    dic = json.loads(string)
    return dic


def store_data(data):
    key = bytes(encrypter.get_new_key(), 'ascii')
    drive_api.set_data('key.txt', key.decode('ascii'))
    e_data = (encrypter.encrypt(key, json.dumps(
        data).encode('ascii'))).decode('ascii')
    drive_api.set_data('curdata.txt', e_data)


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
loading_frame.grid(row=0, column=0, sticky="NSEW")

loading_frame.rowconfigure(0, weight=2)
loading_frame.columnconfigure(0, weight=2)
ttk.Label(loading_frame, text="Loading...").grid(
    row=0, column=0, sticky="NSEW")


# making new object with get ethod to continue in for loop
class similar_entry:
    def __init__(self, name) -> None:
        self.name = name

    def get(self):
        return self.name


# windows for saved data
def show_saved_data():
    global main_data
    
    show_data_frame = tk.Frame()
    show_data_frame.grid(row=0, column=0, sticky="NSEW")
    show_data_frame.tkraise()
    padding_x, padding_y = 10, (5, 5)
    btn_back = ttk.Button(show_data_frame, text="Back", command=startmainapp)
    btn_back.grid(row=0, column=3, sticky='e')
    labmain = ttk.Label(show_data_frame, text='Get Saved Data Of App',
                        justify='center', font=("Arial", 15))
    labmain.grid(row=1, column=0, columnspan=4, padx=padding_x, pady=padding_y)

    # adding weight
    show_data_frame.columnconfigure(0, weight=4)
    show_data_frame.columnconfigure(1, weight=4)
    # show_data_frame.columnconfigure(2, weight=2)
    # show_data_frame.columnconfigure(3, weight=2)

    show_data_frame.rowconfigure(0, weight=1)
    show_data_frame.rowconfigure(1, weight=2)
    show_data_frame.rowconfigure(2, weight=2)

    def show_selected(*args):
        global row_var
        name_of_app = selected_key.get()
        data_app = main_data[name_of_app]
        row_var = 3
        global name_edited
        name_edited = False
        name_list.destroy()
        name_label_selected = ttk.Label(show_data_frame, text=name_of_app)
        name_label_selected.grid(
            row=2, column=1, padx=padding_x, pady=padding_y)
        name_edit_entry = ttk.Entry(show_data_frame)

        def edit_main_app_name():
            global name_edited
            name_label_selected.destroy()
            name_edit_entry.insert(0, name_of_app)
            name_edit_entry.grid(row=2, column=1)
            name_edited = True

        def delet_main_app_data():
            if messagebox.askokcancel('My Password Wallet', f'Do you really want to delete {name_of_app} from saved data.\nThis operation is irreversiable'):
                main_data.pop(name_of_app)
                store_data(main_data)
                startmainapp(f'{name_of_app} Data deleted', color='red')

            else:
                pass

        main_key_edit = ttk.Button(
            show_data_frame, image=edit_image, command=edit_main_app_name)
        CreateToolTip(main_key_edit,'Edit')
        main_key_delete = ttk.Button(
            show_data_frame, image=delete_image, command=delet_main_app_data)
        CreateToolTip(main_key_delete,'Delete')
        main_key_edit.grid(row=2, column=2)
        main_key_delete.grid(row=2, column=3)
        row_lists = []
        new_field_list = []

        def edit_app_data(e):
            # global row_lists
            data_key_name, row_now, key_data = e
            key_edit_entry = ttk.Entry(show_data_frame)
            key_edit_entry.insert(0, data_app[data_key_name])
            key_edit_entry.grid(row=row_now, column=1)
            key_data.destroy()
            row = [data_key_name, key_edit_entry]
            row_lists.append(row)
            # key_edit.config(state='disabled')

        def delete_app_data(e):
            data_key_name, row_no = e
            for row in row_lists:
                if row[0] == data_key_name:
                    row_lists.remove(row)
            data_app.pop(data_key_name)
            row_elements = show_data_frame.grid_slaves(row=row_no)
            for row_element in row_elements:
                row_element.destroy()

        def save_edited():
            for row in row_lists:
                key = row[0]
                data = row[1].get()
                data_app[key] = data
            for nf_row in new_field_list:
                nf_key = nf_row[0].get()
                nf_data = nf_row[1].get()
                data_app[nf_key] = nf_data
            if name_edited:
                new_name = name_edit_entry.get()
                main_data[new_name] = main_data[name_of_app]
                main_data.pop(name_of_app)
            store_data(main_data)
            startmainapp('Data Saved to Google Drive')

        for key in data_app:
            if key != 'Password':
                key_label = ttk.Label(show_data_frame, text=key)
                key_data = ttk.Label(show_data_frame, text=data_app[key])
                key_edit = ttk.Button(show_data_frame, image=edit_image, command=lambda e=(
                    key, row_var, key_data): (edit_app_data(e)))
                CreateToolTip(key_edit,"Edit")
                key_delete = ttk.Button(show_data_frame, image=delete_image, command=lambda e=(
                    key, row_var): (delete_app_data(e)))
                CreateToolTip(key_delete,'Delete')

                key_label.grid(row=row_var, column=0)
                key_data.grid(row=row_var, column=1)
                key_edit.grid(row=row_var, column=2)
                key_delete.grid(row=row_var, column=3)
                show_data_frame.rowconfigure(row_var, weight=2)
                row_var += 1
        else:
            key = 'Password'

            def edit_app_data_password(e):
                # global row_lists
                data_key_name, row_now, key_data, key_edit_entry = e
                key_edit_entry.insert(0, data_app[data_key_name])
                key_edit_entry.grid(row=row_now, column=1)
                key_data.destroy()
                row = [data_key_name, key_edit_entry]
                row_lists.append(row)
                pw_key_label.config(state='disabled')
                pw_key_label.config(text="Password")
                pw_key_edit.config(state='disabled')

            def show_password():
                pw_key_data.config(text=data_app[key])
                pw_key_label.config(text="Hide Password")
                pw_key_label.config(command=hide_password)
                # pw_key_edit_entry.config(show=None)

            def hide_password():
                pw_key_data.config(text=len(data_app[key])*'*')
                pw_key_label.config(text="Show Password")
                pw_key_label.config(command=show_password)
                # pw_key_edit_entry.config(show='*')

            pw_key_label = ttk.Button(
                show_data_frame, text="Show Password", command=show_password)
            pw_key_data = ttk.Label(
                show_data_frame, text=len(data_app[key])*'*')
            pw_key_edit_entry = ttk.Entry(show_data_frame)
            pw_key_edit = ttk.Button(show_data_frame, image=edit_image, command=lambda e=(
                key, row_var, pw_key_data, pw_key_edit_entry): (edit_app_data_password(e)))
            CreateToolTip(pw_key_edit,"Edit")
            pw_key_delete = ttk.Button(show_data_frame, image=delete_image, command=lambda e=(
                key, row_var): (delete_app_data(e)))
            CreateToolTip(pw_key_delete,'Delete')

            pw_key_label.grid(row=row_var, column=0)
            pw_key_data.grid(row=row_var, column=1)
            pw_key_delete.grid(row=row_var, column=3)
            pw_key_edit.grid(row=row_var, column=2)
            show_data_frame.rowconfigure(row_var, weight=2)
            row_var += 1

        def add_new_filed():
            global row_var
            new_field_name = ttk.Entry(show_data_frame)
            new_field_value = ttk.Entry(show_data_frame)
            new_field_name.grid(row=row_var, column=0)
            new_field_value.grid(row=row_var, column=1)
            show_data_frame.rowconfigure(row_var, weight=2)
            row_var += 1
            new_field_list.append([new_field_name, new_field_value])
            add_new_btn.grid(row=row_var, column=0, columnspan=1)
            save_btn.grid(row=row_var, column=1, columnspan=2)

        add_new_btn = ttk.Button(
            show_data_frame, text="Add new field", command=add_new_filed)
        add_new_btn.grid(row=row_var, column=0, columnspan=1)
        save_btn = ttk.Button(
            show_data_frame, text="Save", command=save_edited)
        save_btn.grid(row=row_var, column=1, columnspan=2)

    lab1 = ttk.Label(show_data_frame, text='Name of website or App')
    lab1.grid(row=2, column=0, padx=padding_x, pady=padding_y)

    datafilds = [name for name in main_data.keys()]
    selected_key = tk.StringVar()

    name_list = ttk.Combobox(
        show_data_frame, values=datafilds, textvariable=selected_key, state='readonly')
    name_list.grid(row=2, column=1, padx=padding_x, pady=padding_y)
    name_list.bind('<<ComboboxSelected>>', show_selected)


# window to addd new data
def add_new_data():
    global main_data

    add_data_frame = tk.Frame()
    add_data_frame.grid(row=0, column=0, sticky="NSEW")
    add_data_frame.tkraise()
    padding_x, padding_y = 10, (5, 5)
    labmain = ttk.Label(add_data_frame, text='Enter Details Below',
                        justify='center', font=("Arial", 15))
    labmain.grid(row=1, column=0, columnspan=3, padx=padding_x, pady=padding_y)

    # adding weight
    add_data_frame.columnconfigure(0, weight=2)
    add_data_frame.columnconfigure(1, weight=2)

    add_data_frame.rowconfigure(0, weight=1)
    add_data_frame.rowconfigure(1, weight=3)
    add_data_frame.rowconfigure(2, weight=2)

    right_image = ImageTk.PhotoImage(
        (Image.open('files/right.png')).resize((20, 20), Image.ANTIALIAS))
    wrong_image = ImageTk.PhotoImage(
        (Image.open('files/wrong.png')).resize((20, 20), Image.ANTIALIAS))

    datanames = []
    datavalue = []

    def check_name(*args):
        main_name = name_entry.get()
        if main_name in main_data.keys() or main_name == '':
            status_lab.config(image=wrong_image)
            submit_new_data.config(state='disabled')
        else:
            status_lab.config(image=right_image)
            submit_new_data.config(state='!disabled')

    lab1 = ttk.Label(add_data_frame, text='Name of website or App')
    lab1.grid(row=2, column=0, padx=padding_x, pady=padding_y)
    name_entry = ttk.Entry(add_data_frame)
    name_entry.grid(row=2, column=1, padx=padding_x, pady=padding_y)
    name_entry.bind("<KeyRelease>", check_name)

    status_lab = ttk.Label(add_data_frame, justify='left')
    status_lab.grid(row=2, column=2, padx=padding_x, pady=padding_y)

    # data addition function to store to drive
    def add_data():
        global main_data
        main_name = name_entry.get()
        sub_dict = {}
        for index in range(len(datavalue)):
            data_n, data_e = datanames[index], datavalue[index]
            sub_dict[data_n.get().title()] = data_e.get()
        main_data[main_name] = sub_dict
        store_data(main_data)
        messagebox.showinfo('My Password Wallet',
                            'Data Saved Successfully to Google Drive.')
        startmainapp(message="Data Saved")

    global r
    r = 3
    datafilds = ['Username', 'Email ID',
                 'Mobile Number', 'Password', "Add Other"]
    show_other_name = tk.StringVar()

    def selected_something(*args):
        global r
        name = show_other_name.get()
        if name == 'Add Other':
            data_name = ttk.Entry(add_data_frame)
            data_name.grid(row=r, column=0, padx=padding_x, pady=padding_y)
            data_entry = ttk.Entry(add_data_frame)
            data_entry.grid(row=r, column=1, padx=padding_x, pady=padding_y)

            datanames.append(data_name)
            datavalue.append(data_entry)

        elif name == "Password":
            data_name = ttk.Label(add_data_frame, text=name)
            data_name.grid(row=r, column=0, padx=padding_x, pady=padding_y)
            data_name_entry = similar_entry(name)
            data_entry = ttk.Entry(add_data_frame, show='*')
            data_entry.grid(row=r, column=1, padx=padding_x, pady=padding_y)
            datanames.append(data_name_entry)
            datavalue.append(data_entry)
            datafilds.remove(name)

        else:
            data_name = ttk.Label(add_data_frame, text=name)
            data_name.grid(row=r, column=0, padx=padding_x, pady=padding_y)
            data_name_entry = similar_entry(name)
            data_entry = ttk.Entry(add_data_frame)
            data_entry.grid(row=r, column=1, padx=padding_x, pady=padding_y)
            datanames.append(data_name_entry)
            datavalue.append(data_entry)
            datafilds.remove(name)
        r += 1
        add_data_frame.rowconfigure(r-1, weight=2)
        add_data_frame.rowconfigure(r, weight=2)
        add_data_frame.rowconfigure(r+1, weight=2)

        show_other.grid(row=r, column=0, padx=padding_x, pady=padding_y)
        submit_new_data.grid(row=r+1, column=1, padx=padding_x, pady=padding_y)
        show_other['values'] = datafilds

    show_other = ttk.Combobox(
        add_data_frame, values=datafilds, textvariable=show_other_name, state='readonly')
    show_other.grid(row=r, column=0, padx=padding_x, pady=padding_y)
    show_other.bind('<<ComboboxSelected>>', selected_something)

    submit_new_data = ttk.Button(
        add_data_frame, text="Save data", command=add_data, state='disabled')
    submit_new_data.grid(row=r+1, column=1, padx=padding_x, pady=padding_y)

# main app after main password veri sucess


def startmainapp(message='', color='green'):
    main = tk.Frame(win)
    main.grid(row=0, column=0, sticky="NSEW")
    main.tkraise()

    # defining weights
    main.rowconfigure(0, weight=3)
    main.rowconfigure(1, weight=1)
    main.rowconfigure(2, weight=2)
    main.rowconfigure(3, weight=2)

    main.columnconfigure(0, weight=2)
    # label for main window
    main_label = ttk.Label(
        main, text="Welcome to\nMy Password Wallet", justify='center', font=("Arial", 20))
    main_label.grid(row=0, column=0)

    # define buttons for old data view edit delete
    btnold = ttk.Button(main, text="Get Saved Password",
                        command=show_saved_data)
    btnold.grid(row=2, column=0)

    # to add new data
    btnnew = ttk.Button(main, text="Save New Password", command=add_new_data)
    btnnew.grid(row=3, column=0)

    # messsage to display
    messageonveri = ttk.Label(main, justify='center',
                              foreground=color, font=('arial', 10))
    messageonveri.grid(row=4, column=0, sticky='n', pady=10)

    if message != '':
        messageonveri.config(text=message)
        win.after(3500, lambda: (messageonveri.destroy()))

    # ttk.Label(main,text="Auth Sucess").pack()


def authenticate(pw):
    if verifypass(pw):
        raise_frame(loading_frame)

        # global variable for data
        global main_data
        main_data = get_current_data()
        startmainapp(message='Login Sucessful')
    else:
        oldstart("Wrong Password", color='red')


# for starting new or first time ie show create pass window
def newstart():
    def set():
        global dictraw
        pw1 = pwentry1.get()
        pw2 = pwentry2.get()
        if pw1 != pw2:
            labinfo = ttk.Label(setpass, text='Password Missmatch',
                                justify='center', background='red')
            labinfo.grid(row=3, column=0, columnspan=2, sticky="nsew")
            win.after(3500, lambda: (labinfo.destroy()))
        else:
            if messagebox.askokcancel('Confermation', "Do you really want to set this password \nThis operation is ireversiable."):
                sethash(pw1)
                oldstart("Password created Sucessfully")
            else:
                newstart()
    setpass = tk.Frame(win)
    setpass.grid(row=0, column=0, sticky='NSEW')
    setpass.tkraise()

    setpass.columnconfigure(0, weight=2)
    setpass.rowconfigure(0, weight=2)
    setpass.rowconfigure(1, weight=1)
    setpass.rowconfigure(2, weight=1)
    # setpass.rowconfigure(3,weight=1)
    setpass.rowconfigure(4, weight=2)
    mainlab = ttk.Label(setpass, text="Create New Password",
                        justify='center', font=("Arial", 15))
    mainlab.grid(row=0, column=0, columnspan=2)

    pwlab1 = ttk.Label(setpass, text='Enter New Password')
    pwlab1.grid(row=1, column=0, sticky="esn")
    pwentry1 = ttk.Entry(setpass, show='*')
    pwentry1.grid(row=1, column=1, sticky="EW", padx=30)

    pwlab2 = ttk.Label(setpass, text='Confirm   Password')
    pwlab2.grid(row=2, column=0, sticky="esn")
    pwentry2 = ttk.Entry(setpass, show='*')
    pwentry2.grid(row=2, column=1, sticky="EW", padx=30)

    setbtn = ttk.Button(setpass, text="set", command=set)
    setbtn.grid(row=4, column=0, columnspan=2)


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
        if pw1 != pw2:
            labinfo = ttk.Label(
                reset_password, text='Password Missmatch', justify='center', background='red')
            labinfo.grid(row=4, column=0, columnspan=2, sticky="nsew")
            win.after(3500, lambda: (labinfo.destroy()))
        else:
            if messagebox.askokcancel('Confermation', "This operation is ireversiable And need to reauthenticate with Google\nDo you really want to reset app?",):
                sethash(pw1)
                reset_data()
                messagebox.showinfo(
                    'Password Reset', "Password Reseted Sucessfully.\nWe need to restart the Application.")
                restart_app()
            else:
                reset_password_fun()
    reset_password = tk.Frame(win)
    reset_password.grid(row=0, column=0, sticky='NSEW')
    reset_password.tkraise()
    reset_password.columnconfigure(0, weight=2)
    reset_password.rowconfigure(1, weight=2)
    reset_password.rowconfigure(2, weight=1)
    reset_password.rowconfigure(3, weight=1)
    # reset_password.rowconfigure(4,weight=1)
    reset_password.rowconfigure(5, weight=2)
    mainlab = ttk.Label(reset_password, text="Reset Password",
                        justify='center', font=("Arial", 15))
    mainlab.grid(row=1, column=0, columnspan=2)
    btnback = ttk.Button(reset_password, text="Back", command=oldstart)
    btnback.grid(row=0, column=1, sticky='e', columnspan=1)
    pwlab1 = ttk.Label(reset_password, text='Enter New Password')
    pwlab1.grid(row=2, column=0, sticky="esn")
    pwentry1 = ttk.Entry(reset_password, show='*')
    pwentry1.grid(row=2, column=1, sticky="EW", padx=30)

    pwlab2 = ttk.Label(reset_password, text='Confirm   Password')
    pwlab2.grid(row=3, column=0, sticky="esn")
    pwentry2 = ttk.Entry(reset_password, show='*')
    pwentry2.grid(row=3, column=1, sticky="EW", padx=30)

    resetbtn = ttk.Button(reset_password, text="Reset", command=reset)
    resetbtn.grid(row=5, column=0, columnspan=2)


def darkstyle(root):
    style = ttk.Style(root)
    root.tk.call('source', 'files/theme/azure dark/azure dark.tcl')
    style.theme_use('azure')
    style.configure("Accentbutton", foreground='white')
    style.configure("Togglebutton", foreground='white')
    return style
# style = darkstyle(win)


def oldstart(*args, color='green'):
    if os.path.exists('files/hash.txt'):
        first = True

        def click(*args, first=first):
            if first or pwentry.get() == 'Enter Main Password':
                first = False
                pwentry.delete(0, 'end')
                pwentry.config(show='*')

        def leave(*args):
            if pwentry.get() == '':
                pwentry.insert(0, 'Enter Main Password')
                pwentry.config(show=None)

        verification = tk.Frame(win)
        verification.grid(row=0, column=0, sticky='NSEW')

        verification.columnconfigure(0, weight=2)
        verification.columnconfigure(1, weight=2)
        verification.rowconfigure(0, weight=2)
        verification.rowconfigure(1, weight=1)
        verification.rowconfigure(2, weight=2)
        verification.rowconfigure(3, weight=1)
        mainlab = ttk.Label(
            verification, text="Welcome To Password Wallet", justify='center', font=("Arial", 15))
        mainlab.grid(row=0, column=0, columnspan=2)

        pwentry = ttk.Entry(verification, show=None)
        pwentry.insert(0, 'Enter Main Password')
        pwentry.grid(row=1, column=0, sticky="EW", padx=30, columnspan=2)
        # pwshohidebtn = ttk.Button(verification,text="Show",command=showhide)
        # pwshohidebtn.grid(row=1,column=1,sticky="W")
        pwentry.bind("<Button-1>", click)
        pwentry.bind("<Leave>", leave)

        forgotpwbtn = ttk.Button(
            verification, text="Forgot Password", command=reset_password_fun)
        forgotpwbtn.grid(row=2, column=0)

        messageonveri = ttk.Label(
            verification, justify='center', foreground=color, font=('arial', 10))
        messageonveri.grid(row=4, column=0, sticky='n', pady=10, columnspan=2)

        veribtn = ttk.Button(verification, text="Authenticate",
                             command=lambda: (authenticate(pwentry.get())))
        veribtn.grid(row=2, column=1)

        # rsbtn = ttk.Button(verification,text="Reset App")
        # rsbtn.grid(row=3,column=0,sticky='n',columnspan=2)

        if len(args) == 1:
            messageonveri.config(text=args[0])
            win.after(3500, lambda: (messageonveri.destroy()))
        raise_frame(verification)
    else:
        newstart()


def set_theme(thm):
    with open("files/theme.txt", 'w') as thm_file:
        thm_file.write(thm)


def get_theme():
    if os.path.exists("files/theme.txt"):
        with open("files/theme.txt", 'r') as thm_file:
            thm = thm_file.read()
            if thm in ['light', 'dark']:
                return thm
            else:
                set_theme('light')
                return 'light'
    else:
        set_theme('light')
        return 'light'


bottom_bar = tk.Frame(win)
bottom_bar.grid(row=1, column=0, sticky='nsew')
bottom_bar.tkraise()

# Set the initial theme
win.tk.call("source", "files/theme/sunvallydark-white/sun-valley.tcl")
win.tk.call("set_theme", get_theme())

# images
light_image = ImageTk.PhotoImage(
    (Image.open('files/light.png')).resize((20, 20), Image.ANTIALIAS))
dark_image = ImageTk.PhotoImage(
    (Image.open('files/dark.png')).resize((20, 20), Image.ANTIALIAS))


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
button_chng_thm = ttk.Button(
    bottom_bar, command=change_theme, compound='center')
button_chng_thm.pack(side='left')
if get_theme() == 'light':
    button_chng_thm.config(image=dark_image)
else:
    button_chng_thm.config(image=light_image)

if __name__ == '__main__':
    oldstart()

win.mainloop()
