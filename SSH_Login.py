import tkinter as tk
import paramiko
import script

check = False

root = tk.Tk()

Host = tk.StringVar()
Host.set("lyra.qut.edu.au")

Username = tk.StringVar()
Username.set("n9960392")

Password = tk.StringVar()

def Connect():
    # print(Host.get())
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(Host.get(),username = Username.get(),password = Password.get())
        status =  ssh_client.get_transport().is_active()
        
        if(status):
            root.withdraw()
            script.Main(ssh_client,root)


    except Exception as e:
        print(e)   


def Main():
    #Host,Username and pass
    tk.Label(root,text="Host").grid(row=0)
    tk.Entry(root,textvariable=Host).grid(row = 0,column = 1)

    tk.Label(root,text="Username").grid(row=1)
    tk.Entry(root,textvariable=Username).grid(row = 1,column = 1)

    tk.Label(root,text="Password").grid(row=2)
    tk.Entry(root,textvariable=Password, show="*").grid(row = 2,column = 1)

    #Login button
    tk.Button(root,text="Login",command=Connect).grid(row = 3,column = 2)

    root.mainloop()

