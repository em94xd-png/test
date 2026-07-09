import customtkinter
from tkinter import *
from CTkMessagebox import CTkMessagebox
import sys
import requests
from packaging import version
import os

CURRENT_VERSION = "2.0.0"
URL = "https://raw.githubusercontent.com/em94xd-png/test/refs/heads/main/version.json"

def verify_and_check_version():
    try:
        response = requests.get(URL, timeout=5)
        response.raise_for_status()
        server_data = response.json()
        
        latest_version = server_data["latest_version"]

        if version.parse(CURRENT_VERSION) < version.parse(latest_version):
            show_error_and_exit(
                "จำเป็นต้องอัปเดต!", 
                f"แอปเวอร์ชันนี้เก่าเกินไป ({CURRENT_VERSION})\n"
                f"กรุณาปิดแล้วเปิดผ่าน Launcher.exe เพื่อทำการอัปเดตระบบอัตโนมัติ"
            )
    except requests.RequestException:
        show_error_and_exit("การเชื่อมต่อล้มเหลว", "ไม่สามารถตรวจสอบเวอร์ชันล่าสุดได้\nกรุณาเชื่อมต่ออินเทอร์เน็ต")

def show_error_and_exit(title, message):
    """ฟังก์ชันช่วยสร้างกล่องข้อความเตือนแบบโมเดิร์นแล้วปิดโปรแกรม"""
    root = customtkinter.CTk()
    root.withdraw() # ซ่อนหน้าต่างหลักแอป
    CTkMessagebox(title=title, message=message, icon="cancel")
    root.mainloop()
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

    # btn3 = customtkinter.CTkButton(master=frame)
    # btn3.pack(pady=(0, 10))

    dp = customtkinter.CTkComboBox(master=frame)
    dp.pack()

    wd.mainloop()

if __name__== "__main__":
    verify_and_check_version() # บังคับเช็กด่านความปลอดภัยก่อนเริ่มแอป
    start_main_app()