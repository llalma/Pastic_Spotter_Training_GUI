# import script
import SSH_Login
import os
import tkinter as tk
from tkinter import Button, filedialog

#main method
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

root = tk.Tk()

SSH_Login.Main()

#Run program
root.mainloop()