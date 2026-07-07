import customtkinter
from tkinter import *



wd = customtkinter.CTk()
wd.geometry("1500+300")

k_var = StringVar()

def mode():
    get_var = k_var.get()
    if get_var == "on":
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")

frame = customtkinter.CTkFrame(master=wd)
frame.pack()

sw = customtkinter.CTkSwitch(master=frame, variable=k_var, command=mode, onvalue="on", offvalue="off")
sw.pack()

btn1 = customtkinter.CTkButton(master=frame)
btn1.pack(pady=10)

# btn2 = customtkinter.CTkButton(master=frame)
# btn2.pack(pady=(0,10))

# btn3 = customtkinter.CTkButton(master=frame)
# btn3.pack(pady=(0, 10))

dp = customtkinter.CTkComboBox(master=frame)
dp.pack()

wd.mainloop()