from tkinter import *

window = Tk()

photo = PhotoImage(file="../resources/new.png")
window.geometry("900x500")

button = Button(window)
window.title("Graph")
window.config(background="#34ebdb")
label = Label(window, text="Hello World",
              font=('Arial', 40, 'bold'),
              fg='green',
              bg="#34ebdb",
              relief=RAISED,
              bd=10,
              padx=20,
              pady=20,
              image=photo,
              compound='bottom')
label.place(x=100, y=100)

window.mainloop()