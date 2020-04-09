import tkinter as tk
from tkinter import filedialog
import os
import time
import re

#variables
root = tk.Tk()
root.withdraw()

path = tk.StringVar()
path.set(os.getcwd())

mode = tk.IntVar()
mode.set(0)

project_name = tk.StringVar()
project_name.set("trashnet")

def Create_List(folder_spec):
    #Creates list files from specified folders and all subfolders.

    if folder_spec.upper() == 'TRAIN' or folder_spec.upper() == 'TEST'  :
        #train
        folder = path.get() + '\\data\\training_set\\images\\' + folder_spec
        file = open(path.get() +"\\data\\training_set\\"+folder_spec+".list","w")
    else:
        #predict
        folder = path.get() + '\\run\\predict\\'
        file = open(path.get() +"\\run\\predict.list","w")
    #end

    file.truncate()

    for root, dirs, files in os.walk(folder):
        for name in files:
            if name.endswith((".jpg",".JPG")):
                file.write(name+"\n")
            #end
        #end
    #end
   
    file.close()
#end

def Create_project_data_file():
    text = ["classes = 5\n",
        "train   =  "+ path.get() + '\\data\\training_set\\train.list\n',
        "valid   =  "+ path.get() + '\\data\\training_set\\test.list\n',
        "names   =  "+ path.get() + '\\data\\'+project_name.get()+'.names\n',
        "backup  =  "+ path.get() + '\\data\\training_set\\weights\\\n']

    file = open(path.get() + "\\data\\"+project_name.get()+".data","w")
    file.truncate()

    file.writelines(text)
    file.close()


def run():
    Create_List("train")
    Create_List("test")
    Create_List('predict')
    Create_project_data_file()

    os.chdir(path.get())

    if mode.get() == 0:
        #train
        os.system("start /B start cmd.exe @cmd /k ./darknet detector train ../data/training_set/"+project_name.get()+".data ../data/"+project_name.get()+".cfg ../data/"+project_name.get()+".weights")
    else:
        #predict
        os.system("start /B start cmd.exe @cmd /k ./darknet detector test ../data/training_set/"+project_name.get()+".data ../data/"+project_name.get()+".cfg ../data/"+project_name.get()+".weights < predict.list")
    #end
#end


def Folder_browse():
    path.set(filedialog.askdirectory())
#end


def Main():
    root.update()
    root.deiconify()

    tk.Label(root,text="Darknet Folder").grid(row=0,column=0)
    tk.Entry(root,textvariable = path).grid(row=1,column=1)
    tk.Button(root,text="Browse",command = Folder_browse).grid(row=1,column=0)

    tk.Label(root,text="Project Name").grid(row=2,column=0)
    tk.Entry(root,textvariable = project_name).grid(row=2,column=1)

    tk.Radiobutton(root, text="Train", variable=mode, value=0).grid(row=3,column=0)
    tk.Radiobutton(root, text="Predict", variable=mode, value=1).grid(row=3,column=1)

    tk.Label(root,text="Run").grid(row=4,column=0)
    tk.Button(root,text="Run",command = run).grid(row=4,column=1)
#end