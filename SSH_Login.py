import tkinter as tk
import paramiko
import ssh_script
import local_script

check = False

root = tk.Tk()

#Variables
ssh = tk.BooleanVar()
ssh.set(False)
Host = tk.StringVar()
Host.set("lyra.qut.edu.au")
Username = tk.StringVar()
Username.set("n9960392")
Password = tk.StringVar()

#User inputs
host_box = tk.Entry(root,textvariable=Host,state=tk.DISABLED)
user_box = tk.Entry(root,textvariable=Username,state=tk.DISABLED)
password_box = tk.Entry(root,textvariable=Password, show="*",state=tk.DISABLED)

def Connect():
    #Uses appropriate script if using local or SSH, logs into host, using username and password if conencting to ssh.

    if(ssh.get()):
        #SSH instance
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(Host.get(),username = Username.get(),password = Password.get())
            status =  ssh_client.get_transport().is_active()
            
            if(status):
                root.withdraw()
                ssh_script.Main(ssh_client,root)
            #end
        #end
        except Exception as e:
            print(e)
        #end
    else:
        #Local Instance
        root.withdraw()
        local_script.Main()
    #end   
#end

def selected1():
    #enables and disables inputs if using ssh.
    selected = ssh.get()

    host_box.config(state=tk.DISABLED if selected == False else tk.NORMAL)
    user_box.config(state=tk.DISABLED if selected == False else tk.NORMAL)
    password_box.config(state=tk.DISABLED if selected == False else tk.NORMAL)
#end


def Main():
    #Host,Username and pass
    tk.Checkbutton(root,variable=ssh,text='SSH',command = selected1).grid(row = 0,column = 0)

    tk.Label(root,text="Host").grid(row=1)
    host_box.grid(row = 1,column = 1)

    tk.Label(root,text="Username").grid(row=2)
    user_box.grid(row = 2,column = 1)

    tk.Label(root,text="Password").grid(row=3)
    password_box.grid(row = 3,column = 1)

    #Login button
    tk.Button(root,text="Login",command=Connect).grid(row = 4,column = 2)

    root.mainloop()
#end

