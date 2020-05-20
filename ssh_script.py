import tkinter as tk
from tkinter import filedialog
import os
import paramiko
import time
import re
import math

Username = ''

def Create_Batch(Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,GPU_type):
    with open("batch.sh", "r+") as f:
        txt = f.readlines()
        f.seek(0)

        f.write("#!/usr/bin/env bash\n#PBS -N install_packages\n#PBS -l ncpus="+str(CPU_Amount.get())+"\n#PBS -l mem="+str(RAM_Amount.get())+"GB\n#PBS -l walltime="+str(Run_Time.get())+":00:00\n#PBS -l ngpus="+str(GPU_Amount.get())+"\n#PBS -l gputype="+str(GPU_type.get())+"\n#PBS -o bt_20000_stdout.out\n#PBS -e bt_20000_stderr.out\n")
        line_num = 0
        for line in enumerate(txt):
            line_num+=1
            if(line_num == 78):
                f.write("    ./../darknet detector train ../data/training_set/trashnet.data ../data/trashnet.cfg ../data/trashnet.weights\n")
            elif(line_num > 9):
                f.write(str(line[1]))
        f.close()

def Create_Batch_Predict(Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,GPU_type):
    with open("batch.sh", "r+") as f:
        txt = f.readlines()
        f.seek(0)

        f.write("#!/usr/bin/env bash\n#PBS -N install_packages\n#PBS -l ncpus="+str(CPU_Amount.get())+"\n#PBS -l mem="+str(RAM_Amount.get())+"GB\n#PBS -l walltime="+str(Run_Time.get())+":00:00\n#PBS -l ngpus="+str(GPU_Amount.get())+"\n#PBS -l gputype="+str(GPU_type.get())+"\n#PBS -o bt_20000_stdout.out\n#PBS -e bt_20000_stderr.out\n")
        line_num = 0
        for line in enumerate(txt):
            line_num+=1
            if(line_num == 78):
                f.write("    ./../darknet detector test ../data/training_set/trashnet.data ../data/trashnet.cfg ../data/trashnet.weights < predict.list > result.txt\n")
            elif(line_num > 9):
                f.write(str(line[1]))
        f.close()

def Create_List(ssh_client,username):
    #Split 70 ,30
    folder = "/home/"+username+"/Plastic_Spotter/data/training_set/"
    
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("find "+folder+" -iregex '.+\.jpg'")

    paths = ssh_stdout.readlines() 
    file = open("train.list","w")
    file.truncate()

    #Calculate split
    num_in_train = int(math.floor(len(paths) * 0.7))
    train_paths = paths[0:num_in_train]
    test_paths = paths[num_in_train:-1]
    #Remove path preceding current directory
    file.writelines(train_paths)
    file.close()



    file = open("test.list","w")
    file.truncate()

    #Remove path preceding current directory
    file.writelines(test_paths)

    file.close()

def Create_List_Predict(ssh_client,username):

    folder = "/home/"+username+"/Plastic_Spotter/run/predict/"
    
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("find "+folder+" -iregex '.+\.jpg'")

   
    file = open("predict.list","w")
    file.truncate()

    #Remove path preceding current directory
    file.writelines(ssh_stdout.readlines())

    file.close()

def Create_trashnet5_file(ssh_client,username):
    text = ["classes = 5\n",
        "train   =  /home/"+username+"/Plastic_Spotter/data/training_set/train.list\n",
        "valid   =  /home/"+username+"/Plastic_Spotter/data/training_set/test.list\n",
        "names   =  /home/"+username+"/Plastic_Spotter/data/trashnet.names\n",
        "backup  =  /home/"+username+"/Plastic_Spotter/data/training_set/weights/\n"]

    file = open("trashnet5.data","w+")
    file.truncate()

    file.writelines(text)
    file.close()

def Transfer(ssh_client,username):
    #Transfer batch file to HPC

    sftp = ssh_client.open_sftp()
    sftp.put(str(os.getcwd())+"\\batch.sh", "/home/"+username+"/Plastic_Spotter/run/batch.sh")

    #Transfer test list file to HPC
    sftp.put(str(os.getcwd())+"\\train.list", "/home/"+username+"/Plastic_Spotter/data/training_set/train.list")

    #Transfer test list file to HPC
    sftp.put(str(os.getcwd())+"\\test.list", "/home/"+username+"/Plastic_Spotter/data/training_set/test.list")

    #Transfer predict list file to HPC
    sftp.put(str(os.getcwd())+"\\predict.list", "/home/"+username+"/Plastic_Spotter/run/predict.list")

    #Transfer trashnet5.txt to HPC
    sftp.put(str(os.getcwd())+"\\trashnet5.data", "/home/"+username+"/Plastic_Spotter/data/training_set/trashnet.data")

    #Convert windows line endii=ngs to unix line endings
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("cd Plastic_Spotter/data/training_set;dos2unix test.list; dos2unix train.list; dos2unix trashnet.data")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("cd Plastic_Spotter/run ;dos2unix batch.sh")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("cd Plastic_Spotter/run ;dos2unix predict.list")
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("cd /home/"+username+"/trashnet/data/training_set;dos2unix trashnet.data")
    

    #Wait 3 secs to ensure transfer is complete
    time.sleep(3)

    print('Succesfully sent to server')
#end
        
#Request_Resources program using variables
def Request_Resources(ssh_client,Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,GPU_type,username,root):
    Create_Batch(Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,GPU_type)
    Create_List(ssh_client,username)
    Create_List_Predict(ssh_client,username)
    Create_trashnet5_file(ssh_client,username)
    
    #Transfer created files to HPC
    Transfer(ssh_client,username)

    #Execute batch script
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("cd Plastic_Spotter/run; qsub batch.sh")

    ssh_client.close()
    root.destroy()

#Predict
def Predict(ssh_client,Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,GPU_type,username,root):
    Create_Batch_Predict(Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,GPU_type)
    Create_List(ssh_client,username)
    Create_List_Predict(ssh_client,username)
    Create_trashnet5_file(ssh_client,username)
    
    #Transfer created files to HPC
    Transfer(ssh_client,username)

    #Execute batch script
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("cd Plastic_Spotter/run; qsub batch.sh")

    ssh_client.close()
    root.destroy()

def Main(ssh_client,root,username):
    t = tk.Toplevel(root)
    Username = username

    #Resource Variables
    Run_Time = tk.IntVar()
    Run_Time.set(4)
    RAM_Amount = tk.IntVar()
    RAM_Amount.set(64)
    CPU_Amount = tk.IntVar()
    CPU_Amount.set(1)
    GPU_Amount = tk.IntVar()
    GPU_Amount.set(1)
    GPU_type = tk.StringVar()
    GPU_type.set("P100") #can be P100 or M40
    # Folder_Name = tk.StringVar()
    # Folder_Name.set("training_set_1")

    #Folder name on HPC
    # tk.Label(t,text="Folder Name").grid(row=0,sticky="w")
    # tk.Entry(t,textvariable=Folder_Name).grid(row = 0,column = 2)
   
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

    #GPU type
    tk.Label(t,text="GPU Type  (P100,M40)").grid(row=6,stick="w")
    tk.Entry(t,textvariable=GPU_type).grid(row=6,column=2)

    #Num of GPUs
    tk.Label(t,text="Number of GPUs").grid(row=7,sticky="w")
    tk.Entry(t,textvariable=GPU_Amount).grid(row = 7,column = 2)

    #Request_Resources button
    tk.Button(t,text="Train",command= lambda: Request_Resources(ssh_client,Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,GPU_type,username,root)).grid(row = 8,column = 2)

    #Request_Resources button
    tk.Button(t,text="Predict",command= lambda: Predict(ssh_client,Run_Time,RAM_Amount,CPU_Amount,GPU_Amount,GPU_type,username,root)).grid(row = 9,column = 2)