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
def switch():
    if(same_Path.get() == 1):
        entry.config(textvariable = Images_folder_path)
        button["state"] = "disabled"
    else:
        entry.config(textvariable = Coords_folder_path)
        button["state"] = "normal"  

def Create_Batch(Run_Time,RAM_Amount,CPU_Amount,GPU_Amount):
    with open("batch.sh", "r+") as f:
        txt = f.readlines()
        f.seek(0)

        f.write("#!/usr/bin/env bash\n#PBS -N install_packages\n#PBS -l ncpus="+str(CPU_Amount.get())+"\n#PBS -l mem="+str(RAM_Amount.get())+"GB\n#PBS -l walltime="+str(Run_Time.get())+":00:00\n#PBS -l ngpus="+str(GPU_Amount.get())+"\n#PBS -l gputype=P100\n#PBS -o bt_20000_stdout.out\n#PBS -e bt_20000_stderr.out\n")
        line_num = 0
        for line in enumerate(txt):
            line_num+=1
            if(line_num > 9):
                f.write(str(line[1]))
        f.close()


        
#Request_Resources program using variables
def Request_Resources(ssh_client,Run_Time,RAM_Amount,CPU_Amount,GPU_Amount):
    Create_Batch(Run_Time,RAM_Amount,CPU_Amount,GPU_Amount)
    
    #Transfer batch file to HPC
    sftp = ssh_client.open_sftp()
    sftp.put(str(os.getcwd())+"\\batch.sh", "/home/n9960392/_ws/batch.sh"))

    #Change to file location
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("cd _ws/")

    sleep(10)

    #Execute batch script
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("qsub batch.sh")

    ssh_client.close()


def Main(ssh_client):
    #Resource Variables
    Run_Time = tk.IntVar()
    Run_Time.set("00")
    RAM_Amount = tk.IntVar()
    CPU_Amount = tk.IntVar()
    GPU_Amount = tk.IntVar()

    #Images label,entry and button
    tk.Label(t,text="Images Folder").grid(row=0,sticky="w")
    tk.Entry(t,textvariable=Images_folder_path).grid(row = 0,column = 1)
    tk.Button(t,text="...",command=Select_Folder_Images).grid(row = 0,column = 2)

    #Checkboax to enable same path or not
    same_Path = tk.IntVar(value = 1)
    tk.Checkbutton(t, text="Same Folder", variable=same_Path, command=switch).grid(row=1)

    #Coordiantes label,entry and button
    tk.Label(t,text="Coords Folder").grid(row=2,sticky="w")
    button = tk.Button(t,text="...",command=Select_Folder_Coords, state = "disabled")
    button.grid(row = 2,column = 2)
    entry = tk.Entry(t,textvariable=Images_folder_path)
    entry.grid(row = 2,column = 1)

    #Resources

    #CPUs
    tk.Label(t,text="Number of CPUs").grid(row=3,sticky="w")
    tk.Entry(t,textvariable=CPU_Amount).grid(row = 3,column = 2)

    #RAM
    tk.Label(t,text="Amount of RAM").grid(row=4,sticky="w")
    tk.Entry(t,textvariable=RAM_Amount).grid(row = 4,column = 2)

    #Time Hours
    tk.Label(t,text="Run Time (Hours)").grid(row=5,sticky="w")
    tk.Entry(t,textvariable=Run_Time).grid(row = 5,column = 2)

    #Num of GPUs
    tk.Label(t,text="Number of GPUs").grid(row=6,sticky="w")
    tk.Entry(t,textvariable=GPU_Amount).grid(row = 6,column = 2)

    #Request_Resources button
    tk.Button(t,text="Train",command= lambda: Request_Resources(ssh_client,Run_Time,RAM_Amount,CPU_Amount,GPU_Amount)).grid(row = 7,column = 2)

    #Run program
    # root_new.mainloop()
