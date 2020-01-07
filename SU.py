# login.py
from tkinter import *
from tkinter import messagebox
import sql
import SU
#import dashboard
import login

class SignUpWindow:
    def __init__(self):
        self.win = Tk()
        # reset the window and background color
        self.canvas = Canvas(self.win,
                             width=600, height=500,
                             bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2)
        y = int(height / 2 - 500 / 2)
        str1 = "600x500+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        # disable resize of the window
        self.win.resizable(width=False, height=False)

        # change the title of the window
        self.win.title("Welcome | SignUp Window | Administrator")

    def add_frame(self):
        self.frame = Frame(self.win, height=400, width=450)
        self.frame.place(x=80, y=50)

        x, y = 70, 20

        self.img = PhotoImage(file='images/login.png')
        self.label = Label(self.frame, image=self.img)
        self.label.place(x=x+80, y=y+0)

        # now create a login form
        self.label = Label(self.frame, text="Player SignUp")
        self.label.config(font=("Courier", 20, 'bold'))
        self.label.place(x=140, y=y+150)

        self.uidlabel = Label(self.frame, text="User Name:")
        self.uidlabel.config(font=("Courier", 12, 'bold'))
        self.uidlabel.place(x=50, y=y+230)

        self.userid = Entry(self.frame, font='Courier 12')
        self.userid.place(x=170, y=y+230)

        self.pwdlabel = Label(self.frame, text="Password:")
        self.pwdlabel.config(font=("Courier", 12, 'bold'))
        self.pwdlabel.place(x=50, y=y+260)

        self.password = Entry(self.frame, show='*',
                              font='Courier 12')
        self.password.place(x=170, y=y+260)

        self.pwdlabel = Label(self.frame, text="comfirm:")
        self.pwdlabel.config(font=("Courier", 12, 'bold'))
        self.pwdlabel.place(x=50, y=y + 290)

        self.comfirm = Entry(self.frame, show='*',
                              font='Courier 12')
        self.comfirm.place(x=170, y=y + 290)

        self.button = Button(self.frame, text="Signup",
                             font='Courier 15 bold',
                             command=self.signup)
        self.button.place(x=170, y=y + 320)

        self.win.mainloop()

    def signup(self):

        num = int(sql.user_last()[0][0][-2:])
        user_id = 'user' + '%02d' % (num+1)

        # get the data and store it into tuple (data)
        data = (
            user_id,
            self.userid.get(),
            self.password.get()
        )

        # validations
        if self.userid.get() == "":
            messagebox.showinfo("Alert!", "Enter UserID First")
        elif self.password.get() == "":
            messagebox.showinfo("Alert!", "Enter Password First")
        elif self.comfirm.get() == "":
            messagebox.showinfo("Alert!", "Enter Comfirm First")
        elif self.password.get() != self.comfirm.get():
            messagebox.showinfo("Alert!", "Password and Confirm Must Be Same")
        else:
            res = sql.user_signup(data)
            if res:
                messagebox.showinfo("Message", "SignUp Successfully, your UserId is: %s" % (user_id))
                self.win.destroy()
                log = login.LoginWindow()
                log.add_frame()
            else:
                messagebox.showinfo("Alert!", "Wrong username/password")