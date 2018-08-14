from Tkinter import *

root = Tk()

receivedChats = Text(root, bg="white", width=60, height=30, state=NORMAL)
receivedChats.pack()

receivedChats.insert(END, "Ivan")
receivedChats.configure(state=DISABLED)

root.mainloop()