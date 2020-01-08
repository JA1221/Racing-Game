# _*_coding:utf-8_*_
import tkinter as tk
import sql
from tkinter import *

def show(tup):
    root = tk.Tk()
    root.wm_title('歷史成績')
    root.geometry("300x500")
    root.resizable(width=False, height=False)

    fram2 = Frame(root)
    lb = Listbox(fram2, width = 40, height = 30)

    try:
        for i in sql.player_score(tup):
            lb.insert(END, str('Date: '+i[2]+', Score: '+i[1]))
    except:
        print("error")

    lb.pack(side=LEFT)
    sl = Scrollbar(fram2)
    sl.pack(side=RIGHT, fill=Y)
    lb['yscrollcommand'] = sl.set
    sl['command'] = lb.yview

    fram2.pack(side=TOP)

    root.mainloop()