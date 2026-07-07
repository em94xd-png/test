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
version_check_url = "https://raw.githubusercontent.com/em94xd-png/test/refs/heads/main/version.json"

def check_for_updates():
    try:
        response = requests.get(version_check_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        latest_version = data["latest_version"]
        min_version = data["min_version_required"]
        download_url = data["download_url"]

        if version.parse(current_version) < version.parse(min_version):
            messagebox.showerror(message=
                "Need Update!"
                f"Your current version {current_version}\n"
                f"Update to {latest_version}"
            )

            file_name = download_url.split("/")[-1]
            if not file_name.endswith(".exe"):
                file_name = "app_update.exe"

            local_filename = os.path.join(os.getcwd(), file_name)

            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, "wb") as f:
                    for chuck in r.iter_content(chunk_size=8192):
                        f.write(chuck)

            subprocess.Popen([local_filename], shell=True)
            sys.exit()
    
    except (requests.RequestException, KeyError, ValueError, OSError) as e:
        # กรณีเกิดข้อผิดพลาดในการโหลดหรือรันไฟล์ จะบังคับปิดแอปฯ เพื่อความปลอดภัย
        root = customtkinter.CTk()
        root.withdraw()
        CTkMessagebox(
            title="เกิดข้อผิดพลาด",
            message="ไม่สามารถอัปเดตแอปพลิเคชันได้อัตโนมัติ\nกรุณาตรวจสอบการเชื่อมต่ออินเทอร์เน็ตของคุณ",
            icon="cancel"
        )
        sys.exit()

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