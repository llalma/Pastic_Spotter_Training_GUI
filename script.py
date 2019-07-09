import tkinter as tk
from tkinter import filedialog
import os
import paramiko
import time
import re

def Create_Batch(Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,Folder_Name):
    with open("batch.sh", "r+") as f:
        txt = f.readlines()
        f.seek(0)

        f.write("#!/usr/bin/env bash\n#PBS -N install_packages\n#PBS -l ncpus="+str(CPU_Amount.get())+"\n#PBS -l mem="+str(RAM_Amount.get())+"GB\n#PBS -l walltime="+str(Run_Time.get())+":00:00\n#PBS -l ngpus="+str(GPU_Amount.get())+"\n#PBS -l gputype=P100\n#PBS -o bt_20000_stdout.out\n#PBS -e bt_20000_stderr.out\n")
        line_num = 0
        for line in enumerate(txt):
            line_num+=1
            if(line_num == 78):
                f.write("    ./darknet/darknet detector train darknet/data/data.data darknet/data/trashnet.cfg darknet/data/trashnet.weights\n")
            elif(line_num > 9):
                f.write(str(line[1]))
        f.close()

def Create_List(ssh_client,Folder_Name):

    folder = "/home/n9960392/darknet/data/" + Folder_Name.get() + "/images/train"
    
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("find "+folder+" -iregex '.+\.jpg'")

   
    file = open("train.list","w")
    file.truncate()

    #Remove path preceding current directory
    file.writelines(ssh_stdout.readlines())

    file.close()

    folder = "/home/n9960392/darknet/data/" + Folder_Name.get() + "/images/test"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("find "+folder+" -iregex '.+\.jpg'")

    file = open("test.list","w")
    file.truncate()

    #Remove path preceding current directory
    file.writelines(ssh_stdout.readlines())

    file.close()

def Create_trashnet5_file(ssh_client,Folder_Name):
    text = ["classes = 5\n",
        "train   =  _ws/darknet/"+Folder_Name.get()+"/data/train.list\n",
        "valid   =  _ws/darknet/"+Folder_Name.get()+"/data/test.list\n",
        "labels  =  _ws/darknet/"+Folder_Name.get()+"/data/trashnet5.txt\n",
        "names   =  _ws/darknet/"+Folder_Name.get()+"/data/trashnet5.names\n",
        "backup  =  _ws/darknet/"+Folder_Name.get()+"/weights/\n",
        "top     = 2\n"]

    file = open("trashnet5.data","w")
    file.truncate()

    file.writelines(text)
    file.close()

def Transfer(ssh_client,Folder_Name):
    #Transfer batch file to HPC

    sftp = ssh_client.open_sftp()
    sftp.put(str(os.getcwd())+"\\batch.sh", "/home/n9960392/darknet/batch.sh")

    #Transfer test list file to HPC
    sftp.put(str(os.getcwd())+"\\train.list", "/home/n9960392/darknet/data/" + Folder_Name.get() + "/train.list")

    #Transfer test list file to HPC
    sftp.put(str(os.getcwd())+"\\test.list", "/home/n9960392/darknet/data/" + Folder_Name.get() + "/test.list")

    #Transfer trashnet5.txt to HPC
    sftp.put(str(os.getcwd())+"\\trashnet5.data", "/home/n9960392/darknet/data/" + Folder_Name.get() + "/trashnet5.data")

    #Convert windows line endii=ngs to unix line endings
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("cd darknet/data/" + Folder_Name.get() + ";dos2unix test.list; dos2unix train.list")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("cd darknet/ ;dos2unix batch.sh")
    

    #Wait 10 secs to ensure transfer is complete
    time.sleep(3)

        
#Request_Resources program using variables
def Request_Resources(ssh_client,Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,Folder_Name,root):
    Create_Batch(Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,Folder_Name)
    Create_List(ssh_client,Folder_Name)
    Create_trashnet5_file(ssh_client,Folder_Name)
    
    #Transfer created files to HPC
    Transfer(ssh_client,Folder_Name)

    #Execute batch script
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("qsub darknet/batch.sh")

    ssh_client.close()
    root.destroy()

def Main(ssh_client,root):
    t = tk.Toplevel(root)

    #Resource Variables
    Run_Time = tk.IntVar()
    Run_Time.set("4")
    RAM_Amount = tk.IntVar()
    RAM_Amount.set(64)
    CPU_Amount = tk.IntVar()
    CPU_Amount.set(1)
    GPU_Amount = tk.IntVar()
    GPU_Amount.set(1)
    Folder_Name = tk.StringVar()
    Folder_Name.set("training_set_1")

    #Folder name on HPC
    tk.Label(t,text="Folder Name").grid(row=0,sticky="w")
    tk.Entry(t,textvariable=Folder_Name).grid(row = 0,column = 2)
   
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
    tk.Button(t,text="Train",command= lambda: Request_Resources(ssh_client,Run_Time,RAM_Amount,CPU_Amount,GPU_Amount, Folder_Name,root)).grid(row = 7,column = 2)