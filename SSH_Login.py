import tkinter as tk
import paramiko
# import local_script
# import ssh_script


root = tk.Tk()
root.withdraw()
toplevel = tk.Toplevel(root)

#Variables
ssh = tk.BooleanVar()
ssh.set(False)
Host = tk.StringVar()
Host.set("lyra.qut.edu.au")
Username = tk.StringVar()
Username.set("n9960392")
Password = tk.StringVar()

#User inputs
host_box = tk.Entry(toplevel,textvariable=Host,state=tk.DISABLED)
user_box = tk.Entry(toplevel,textvariable=Username,state=tk.DISABLED)
password_box = tk.Entry(toplevel,textvariable=Password, show="*",state=tk.DISABLED)

def Connect():
    #Uses appropriate script if using local or SSH, logs into host, using username and password if conencting to ssh.

    if(ssh.get()):
        mod = __import__('ssh_script')
        func = getattr(mod, 'Main') 
        #SSH instance
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(Host.get(),username = Username.get(),password = Password.get())
            status =  ssh_client.get_transport().is_active()

            
            if(status):
                root.withdraw()
                ssh_script.Main(ssh_client,root,Username.get())
            #end
        #end
        except Exception as e:
            print(e)
        #end
    else:
        #Local Instance
        mod = __import__('local_script')
        func = getattr(mod, 'Main')  
        root.withdraw()
        func()
    #end   
#end

def selected1():
    #enables and disables inputs if using ssh.
    selected = ssh.get()

    host_box.config(state=tk.DISABLED if selected == False else tk.NORMAL)
    user_box.config(state=tk.DISABLED if selected == False else tk.NORMAL)
    password_box.config(state=tk.DISABLED if selected == False else tk.NORMAL)
#end

def enter(event = None):
    #Runs connect on enter button press
    Connect()
#end


def Main():
    #Host,Username and pass
    tk.Checkbutton(toplevel,variable=ssh,text='SSH',command = selected1).grid(row = 0,column = 0)

    tk.Label(toplevel,text="Host").grid(row=1)
    host_box.grid(row = 1,column = 1)

    tk.Label(toplevel,text="Username").grid(row=2)
    user_box.grid(row = 2,column = 1)

    tk.Label(toplevel,text="Password").grid(row=3)
    password_box.grid(row = 3,column = 1)

    #Login button
    tk.Button(toplevel,text="Login",command=Connect).grid(row = 4,column = 2)

    #Bind enter to login button
    toplevel.bind('<Return>',enter)

    toplevel.mainloop()
#end

