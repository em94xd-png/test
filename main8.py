import customtkinter
from tkinter import *
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
import subprocess
import json
import os
import requests
from packaging import version
import webbrowser
import sys

current_version = "1.0.0"
version_check_url = ""

def check_for_updates():
    try:
        response = requests.get(version_check_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        latest_version = data["1.0.0"]
        min_version = data["1.0.0"]
        download_url = data[""]

        if version.parse(current_version) < version.parse(min_version):
            messagebox.showerror(message=
                "Need Update!"
                f"Your current version {current_version}\n"
                f"Update to {latest_version}"
            )

            webbrowser.open(download_url)
            sys.exit
    
    except requests.RequestException as e:
        messagebox.showwarning(message=
            "Cannot!"
        )

def start_main_app():
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

    btn2 = customtkinter.CTkButton(master=frame)
    btn2.pack(pady=(0,10))

    btn3 = customtkinter.CTkButton(master=frame)
    btn3.pack(pady=(0, 10))

    dp = customtkinter.CTkComboBox(master=frame)
    dp.pack()

    wd.mainloop()

if __name__== "__main__":
    check_for_updates()
    start_main_app()