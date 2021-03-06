# login.py
from tkinter import *
from tkinter import messagebox
import sql, SS
import SU
#import dashboard
import RacingGame

class LoginWindow:
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
        self.win.title("Welcome | Login Window | Administrator")

    def add_frame(self):
        self.frame = Frame(self.win, height=400, width=450)
        self.frame.place(x=80, y=50)

        x, y = 70, 20

        self.img = PhotoImage(file='images/login.png')
        self.label = Label(self.frame, image=self.img)
        self.label.place(x=x+80, y=y+0)

        # now create a login form
        self.label = Label(self.frame, text="Player Login")
        self.label.config(font=("Courier", 20, 'bold'))
        self.label.place(x=140, y=y+150)

        self.uidlabel = Label(self.frame, text="User ID:")
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

        self.button1 = Button(self.frame, text="Login",
                             font='Courier 15 bold',
                             command=self.login)
        self.button1.place(x=50, y=y+300)

        self.button2 = Button(self.frame, text="Signup",
                             font='Courier 15 bold',
                             command=self.SU)
        self.button2.place(x=170, y=y + 300)

        self.button3 = Button(self.frame, text="MyScore",
                             font='Courier 15 bold',
                             command=self.getScore)
        self.button3.place(x=300, y=y + 300)

        self.win.mainloop()

    def getScore(self):

        data = (
            self.userid.get(),
            self.password.get()
        )
        # validations
        if self.userid.get() == "":
            messagebox.showinfo("Alert!", "Enter UserID First")
        elif self.password.get() == "":
            messagebox.showinfo("Alert!", "Enter Password First")
        else:
            res = sql.user_login(data)
            if res:
                tup = (self.userid.get(),)
                SS.show(tup)
            else:
                messagebox.showinfo("Alert!", "Wrong username/password")

    def SU(self):

        self.win.destroy()
        x = SU.SignUpWindow()
        x.add_frame()

    def login(self):
        # get the data and store it into tuple (data)
        data = (
            self.userid.get(),
            self.password.get()
        )
        # validations
        if self.userid.get() == "":
            messagebox.showinfo("Alert!", "Enter UserID First")
        elif self.password.get() == "":
            messagebox.showinfo("Alert!", "Enter Password First")
        else:
            res = sql.user_login(data)
            if res:
                messagebox.showinfo("Message", "Login Successfully")
                self.win.destroy()
                # x = dashboard.DashboardWindow()
                x = RacingGame.main(data)
            else:
                messagebox.showinfo("Alert!", "Wrong username/password")
