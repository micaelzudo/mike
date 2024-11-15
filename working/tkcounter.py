import tkinter as tk
from time import sleep

def countdown():
    for i in range(1, 11):
        label.config(text=str(i))
        root.update()
        if i < 10:
            root.after(1000)  # wait 1 second and then call again
        else:
            break

root = tk.Tk()
label = tk.Label(root, font=('Arial', 64), fg='blue')
label.pack()

countdown()
root.mainloop()