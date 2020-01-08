# _*_coding:utf-8_*_
import tkinter as tk
from tkinter import *

if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title('Scrollbar')
    root.geometry("300x500")
    root.resizable(width=True, height=True)

    fram2 = Frame(root)
    lb = Listbox(fram2, width = 30, height = 30)
    for i in range(100):
        lb.insert(END, str(i) + 'listbdgfjkhsagfhksjdgox')

    lb.pack(side=LEFT)
    sl = Scrollbar(fram2)
    sl.pack(side=RIGHT, fill=Y)
    lb['yscrollcommand'] = sl.set
    sl['command'] = lb.yview

    fram2.pack(side=TOP)

    root.mainloop()