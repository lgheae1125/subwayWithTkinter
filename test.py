import tkinter as tk

root = tk.Tk()

idx = 1
img = tk.PhotoImage(file='./images/{0}.png'.format(idx))
label = tk.Label(root, image=img)

label.pack()

root.mainloop()