import tkinter

window = tkinter.Tk()

window.title("GUI")

# tkinter.Label(window, text = "~~ Welcome to your personal banking app ~~").pack()

# tkinter.Label(window, text = "Please enter select one of the options below to proceed").pack()

tkinter.Button(window, text = "Make a deposit").grid(row=0, column=0)

tkinter.Button(window, text= "Make a widraw").grid(row=0, column=1)

window.mainloop()