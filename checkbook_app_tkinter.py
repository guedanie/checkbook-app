import tkinter

window = tkinter.Tk()

window.title("GUI")

tkinter.Label(window, text = "~~ Welcome to your personal banking app ~~").pack()

tkinter.Label(window, text = "Please enter select one of the options below to proceed").pack()

tkinter.Button(window, text = "Make a deposit").pack()

tkinter.Button(window, text= "Make a widraw").pack()

window.mainloop()