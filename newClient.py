#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 18 - xmlrpc_introspect.py
# XML-RPC client
import xmlrpclib
from Tkinter import *
import time
import socket
import thread
import struct
import json
from ttk import *

myclients = {}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 0))
sl.bind(('0.0.0.0', 0))

proxy = xmlrpclib.ServerProxy('http://127.0.0.1:7001')



class ChatClient(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.registerUI()
        self.status = 0
        self.buffsize = 1024
        self.allClients = {}



    def registerUI(self):

        self.root.title("Register")
        registerSizeX = self.root.winfo_screenwidth()
        registerSizeY = self.root.winfo_screenheight()
        self.FrameSizeX = 285
        self.FrameSizeY = 215
        FramePosX = (registerSizeX - self.FrameSizeX) / 2
        FramePosY = (registerSizeY - self.FrameSizeY) / 2
        self.root.geometry("%sx%s+%s+%s" % (self.FrameSizeX, self.FrameSizeY, FramePosX, FramePosY))
        self.root.resizable(width=False, height=True)

        #name field
        nameLabel = Label(self.root, text="Name:")
        self.nameVar = StringVar()
        self.nameVar.set("Enter name")
        nameEntry = Entry(self.root, width=20, textvariable=self.nameVar)
        nameEntry.bind("<Button-1>", self.removeValue)

        #username field
        usernameLabel = Label(self.root, text="Username:")
        self.usernameVar = StringVar()
        self.usernameVar.set("Enter username")
        self.usernameEntry = Entry(self.root, width=20, textvariable=self.usernameVar)
        self.usernameEntry.bind("<Button-1>", self.removeValue1)

        #password Field
        passwordLabel = Label(self.root, text="Password:")
        self.passwordEntry = Entry(self.root, width=20, show="*")
        repasswordLabel = Label(self.root, text="Re-type password")
        self.repasswordEntry = Entry(self.root, width=20, show="*")

        #email Field
        emailLabel = Label(self.root, text="E-mail:")
        emailEntry = Entry(self.root, width=20)

        #Register Button
        registerButton = Button(self.root, text="Register") #enter command for register click

        #Already Logged in
        loginLabel = Label(self.root, text="Already signed in?")
        clickHereLabel = Label(self.root, text="Click here", font=(16)) #bind for command
        clickHereLabel.bind("<Button-1>", self.openLogin)

        nameLabel.grid(row=0, column=0, sticky=E)
        nameEntry.grid(row=0, column=1)
        usernameLabel.grid(row=1, column=0, sticky=E)
        self.usernameEntry.grid(row=1, column=1)
        passwordLabel.grid(row=2, column=0, sticky=E)
        self.passwordEntry.grid(row=2, column=1)
        repasswordLabel.grid(row=3, column=0, sticky=E)
        self.repasswordEntry.grid(row=3, column=1)
        emailLabel.grid(row=4, column=0, sticky=E)
        emailEntry.grid(row=4, column=1)
        registerButton.grid(row=5, columnspan=2, pady=10)
        loginLabel.grid(row=6, columnspan=2)
        clickHereLabel.grid(row=7, columnspan=2)

        registerButton.bind("<Button-1>", self.checkValidity)

    def initUI(self):
        self.chatUI = Toplevel(self.loginWindow)
        self.chatUI.title("Simple P2P Chat Client")
        ScreenSizeX = self.chatUI.winfo_screenwidth()
        ScreenSizeY = self.chatUI.winfo_screenheight()
        self.FrameSizeX = 800
        self.FrameSizeY = 600
        FramePosX = (ScreenSizeX - self.FrameSizeX) / 2
        FramePosY = (ScreenSizeY - self.FrameSizeY) / 2
        self.chatUI.geometry("%sx%s+%s+%s" % (self.FrameSizeX, self.FrameSizeY, FramePosX, FramePosY))
        self.chatUI.resizable(width=False, height=False)

        padX = 10
        padY = 10
        parentFrame = Frame(self.chatUI)
        parentFrame.grid(padx=padX, pady=padY, stick=E+W+N+S)

        ipGroup = Frame(parentFrame)
        ipGroup.pack()
        myAddress = Label(ipGroup, text="Info: ")

        self.nameVar = StringVar()
        self.nameVar.set(self.loginUsernameEntry.get())
        nameField = Entry(ipGroup, width=10, textvariable=self.nameVar)

        self.myIPvar = StringVar()
        self.myIPvar.set(sl.getsockname()[0])
        IPvarField = Entry(ipGroup, width=15, textvariable=self.myIPvar)
        IPvarField.configure(state='readonly')

        self.myPortVar = StringVar()
        self.myPortVar.set(sl.getsockname()[1])
        portField = Entry(ipGroup, width=5, textvariable=self.myPortVar)
        portField.configure(state='readonly')

        self.status = StringVar()
        self.status.set("Online")
        status = Entry(ipGroup, textvariable=self.status, width=10)
        status.configure(state='readonly')

        addClientLabel = Label(ipGroup, text="Add Friend: ")
        self.nameClient = StringVar()
        clientNameField = Entry(ipGroup, width=10, textvariable=self.nameClient)

        logout = Button(ipGroup, text="Log out", width=10, command=self.logOut)

        clientSetButton = Button(ipGroup, text="Add", width=10, command=self.handleAddClient) #dodadi commandHandler
        myAddress.grid(row=0, column=0)
        nameField.grid(row=0, column=1)
        IPvarField.grid(row=0, column=2)
        portField.grid(row=0, column=3)
        status.grid(row=0, column=4)
        addClientLabel.grid(row=0, column=5)
        clientNameField.grid(row=0, column=6)
        clientSetButton.grid(row=0, column=7)
        logout.grid(row=0, column=9)

        readChatGroup = Frame(parentFrame)
        readChatGroup.pack()
        self.receivedChats = Text(readChatGroup, bg="white", width=60, height=30, state=DISABLED)
        self.friends = Listbox(readChatGroup, bg="white", width=30, height=30, selectmode=EXTENDED)
        self.receivedChats.grid(row=0, column=0, sticky=W + N + S, padx=(0, 10))
        self.friends.grid(row=0, column=1, sticky=E + N + S)

        writeChatGroup = Frame(parentFrame)
        writeChatGroup.pack()

        self.chatVar = StringVar()
        self.chatField = Entry(writeChatGroup, width=80, textvariable=self.chatVar)
        sendChatButton = Button(writeChatGroup, text="Send", width=10, command=self.handleSendChat) #commanda za send
        self.chatField.grid(row=0, column=0, sticky=W)
        sendChatButton.grid(row=0, column=1, padx=5)
        # self.handleReading()

        self.friends.bind("<<ListboxSelect>>", self.write)


    def write(self, event):
        self.var = self.friends.get(self.friends.curselection())
        self.friends.get(ACTIVE)
        if self.chatField.get() == "":
            self.chatField.insert(0, str(self.var)+"(private): ")
            print self.chatField.get()
        else:
            self.chatField.delete(0, "")
            self.chatField.insert(0, str(self.var)+"(private): ")
            print self.chatField.get()
        print "I want to send to " + self.var

    def read(self, conn):
        print "na start vlaga"
        while True:
            print "Ceka Konekcija"
            s1, add = conn.accept()
            self.receivedChats.configure(state=NORMAL)
            print add
            data = s1.recv(self.buffsize)
            korisnici = json.loads(proxy.sendAddresses())
            # for users in korisnici:
            #     if tuple(korisnici[users]) == add:
            self.receivedChats.insert(END, data+"\n")
            self.receivedChats.configure(state=DISABLED)

    def handleSendChat(self):
        self.receivedChats.configure(state=NORMAL)
        text = self.chatField.get()
        text = text.split(' ')
        adresa = json.loads(proxy.sendAddresses())
        ime = text[0].split('(')
        if ime[0] in adresa:
            s.connect(tuple(adresa[ime[0]]))
            print "This is the address to send to: "+str(tuple(adresa[ime[0]]))
        del text[0]
        print text
        poraka = " ".join(text)
        s.send(poraka)
        self.receivedChats.insert(END, "You: "+poraka+"\n")
        self.receivedChats.configure(state=DISABLED)
        print poraka
        s.close()

    def logOut(self):
        proxy.removeFromLogged(self.loginUsernameEntry.get())
        self.chatUI.destroy()
    #
    # def handleReceiveChat(self):
    #     sl.listen(1)
    #     thread.start_new_thread(self.read, (sl,))

    def handleAddClient(self):

        registrirani_korisnici = json.loads(proxy.sendRegisteredClients())
        adresinakorisnici = json.loads(proxy.sendAddresses())
        if self.nameClient.get() in myclients.keys():
            print "Already a friend"
        else:
            if self.nameClient.get() in registrirani_korisnici:
                myclients[self.nameClient.get()] = adresinakorisnici[self.nameClient.get()]
                # thread.start_new_thread(self.statusi,())
                self.friends.insert(END, self.nameClient.get())
            else:
                print "he doesn't exist"


    def openLogin(self, event):
        self.loginUI()
        self.root.geometry("%sx%s+%s+%s" % (0, 0, 0, 0))

    def loginUI(self):

        self.loginWindow = Toplevel(self.root)
        self.loginWindow.title("Log in")
        self.loginWindow.geometry("300x290+20+20")
        self.loginWindow.resizable(width=False, height=True)

        upperFrame = Frame(self.loginWindow)
        upperFrame.grid(row=0, column=0, padx=20, pady=30)
        bottomFrame = Frame(self.loginWindow)
        bottomFrame.grid(row=1, column=0)

        #username field
        usernameLabel = Label(upperFrame, text="Username:")
        self.loginUsernameEntry = Entry(upperFrame, width=22)

        #password field
        passwordLabel = Label(upperFrame, text="Password:")
        self.loginPasswordEntry = Entry(upperFrame, width=22, show='*')

        usernameLabel.grid(row=0, column=0, sticky=E)
        self.loginUsernameEntry.grid(row=0, column=1)
        passwordLabel.grid(row=1, column=0, sticky=E)
        self.loginPasswordEntry.grid(row=1, column=1)

        #login Button

        loginButton = Button(bottomFrame, text="Log in", command=self.loginValidity) #command da otvara nov prozorec za chat posle logoinot
        loginButton.grid(row=0, columnspan=2)

    def loginValidity(self):

        registriraniClienti = json.loads(proxy.sendRegisteredClients())
        print registriraniClienti.keys()
        print str(self.loginUsernameEntry.get())+" | "+str(self.loginPasswordEntry.get())+" | "+str(registriraniClienti[self.loginUsernameEntry.get()])
        if self.loginUsernameEntry.get() in registriraniClienti.keys():
            if self.loginPasswordEntry.get() == str(registriraniClienti[self.loginUsernameEntry.get()][0]):
                proxy.logIn(str(self.loginUsernameEntry.get()), str(self.loginPasswordEntry.get()), json.dumps(sl.getsockname()))
                sl.listen(1)
                thread.start_new_thread(self.read, (sl,))
                self.initUI()
            else:
                noMatch = Label(self.loginWindow, text="The password or username didn't match")
                noMatch.grid(row=2, columnspan=2)
        else:
            noMatch1 = Label(self.loginWindow, text="The password or username didn't match")
            noMatch1.grid(row=2, columnspan=2)

    def checkValidity(self, event):

        brojac = 0
        if self.passwordEntry.get() == self.repasswordEntry.get():
            brojac = brojac + 1
        else:
            notMatch = Label(self.root, text="The passwords don\'t match")
            notMatch.grid(row=8, columnspan=2, pady=15)

        registeredClients = json.loads(proxy.sendRegisteredClients())
        if self.usernameEntry.get() not in registeredClients:
            brojac = brojac + 1
        else:
            notMatch1 = Label(self.root, text="The username already exists")
            notMatch1.grid(row=9, columnspan=2)

        if brojac == 2:
            proxy.Register(self.usernameEntry.get(), self.repasswordEntry.get(), json.dumps(sl.getsockname()))
            successfulRegister = Label(self.root, text="You have been successfully registered")
            successfulRegister.grid(row=8, columnspan=2)
            time.sleep(2)
            self.root.geometry("%sx%s+%s+%s" % (0, 0, 0, 0))
            self.loginUI()

    def removeValue(self, event):
        self.nameVar.set("")
        return None

    def removeValue1(self, event):
        self.usernameVar.set("")
        return None

def Main():
    root = Tk()
    app = ChatClient(root)
    root.mainloop()

if __name__ == '__main__':
    Main()
