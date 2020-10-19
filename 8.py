# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:45:43 2020

@author: lenovouser
"""

import tkinter as tk

window = tk.Tk()
window.title('my window')
window.geometry('200x200')
tk.Label(window, text='on the window').pack()

frm = tk.Frame(window)
frm.pack()
frm_l = tk.Frame(frm, )
frm_r = tk.Frame(frm)
frm_l.pack()
frm_r.pack(side='right')

tk.Label(frm_l, text='on the frm_l1').pack()
tk.Label(frm_l, text='on the frm_l2').pack()
tk.Label(frm_r, text='on the frm_r1').pack()
window.mainloop()


