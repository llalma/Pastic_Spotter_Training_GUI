import tkinter as tk
from tkinter import filedialog
import os
import paramiko

#Variables
t = tk.Toplevel()

Images_folder_path = tk.StringVar()
Images_folder_path.set(os.getcwd())
Coords_folder_path = tk.StringVar()
Coords_folder_path.set(os.getcwd())
entry = tk.Entry()
button = tk.Button()
same_Path = tk.IntVar(value = 1)

#Get images location
def Select_Folder_Images():
    Images_folder_path.set(filedialog.askdirectory())
    print(Images_folder_path)
        
#Get coords location
def Select_Folder_Coords():
    Coords_folder_path.set(filedialog.askdirectory())
    print(Coords_folder_path)

#enable and disable button from check box
def switch(ssh_client):
    if(same_Path.get() == 1):
        entry.config(textvariable = Images_folder_path)
        button["state"] = "disabled"
    else:
        entry.config(textvariable = Coords_folder_path)
        button["state"] = "normal"  

#Train program using variables
def Train(ssh_client):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("ls")
    print(ssh_stdout)


def Main(ssh_client):

    #Images label,entry and button
    tk.Label(t,text="Images Folder").grid(row=0)
    tk.Entry(t,textvariable=Images_folder_path).grid(row = 0,column = 1)
    tk.Button(t,text="...",command=Select_Folder_Images).grid(row = 0,column = 2)

    #Checkboax to enable same path or not
    same_Path = tk.IntVar(value = 1)
    tk.Checkbutton(t, text="Same Folder", variable=same_Path, command=switch).grid(row=1)

    #Coordiantes label,entry and button
    tk.Label(t,text="Coords Folder").grid(row=2)
    button = tk.Button(t,text="...",command=Select_Folder_Coords, state = "disabled")
    button.grid(row = 2,column = 2)
    entry = tk.Entry(t,textvariable=Images_folder_path)
    entry.grid(row = 2,column = 1)

    #Train button
    tk.Button(t,text="Train",command= lambda: Train(ssh_client)).grid(row = 3,column = 2)

    #Run program
    # root_new.mainloop()
