import os, sys, subprocess, requests, customtkinter, json
from packaging import version

URL = "https://raw.githubusercontent.com/em94xd-png/test/refs/heads/main/version.json"
MAIN_EXE = os.path.join(os.getcwd(), "main8.exe") # ชื่อไฟล์แอปหลัก
LOCAL_JSON = os.path.join(os.getcwd(), "version.json") # ไฟล์เก็บเวอร์ชันในเครื่อง

def run_launcher():
    # สร้างหน้าต่างแจ้งเตือนโหลดสั้นๆ สีมืดดูโมเดิร์น
    wd = customtkinter.CTk()
    wd.geometry("300x120+400+400")
    wd.title("Launcher")
    
    lbl = customtkinter.CTkLabel(wd, text="กำลังตรวจสอบและอัปเดตระบบ...", font=("Arial", 14))
    lbl.pack(pady=20)

    def process_update():
        try:
            curr_version = "0.0.0"
            if os.path.exists(LOCAL_JSON):
                with open(LOCAL_JSON, "r") as f:
                    curr_version = json.load(f).get("latest_version", "0.0.0")

            # 2. ดึงข้อมูลเวอร์ชันล่าสุดจากออนไลน์
            server_data = requests.get(URL, timeout=5).json()
            latest_version = server_data["latest_version"]

            # 3. ตรวจสอบเงื่อนไข: หากเวอร์ชันในเครื่องเก่ากว่าบนเซิร์ฟเวอร์ ให้ดาวน์โหลดใหม่
            if version.parse(curr_version) < version.parse(latest_version):

                # # ใช้ PowerShell สั่ง taskkill ด้วยสิทธิ์ Admin เสมอ และซ่อนหน้าต่างดำ (-WindowStyle Hidden)
                # cmd_kill = 'powershell -Command "Start-Process taskkill -ArgumentList \'/f\', \'/im\', \'main8.exe\' -Verb RunAs -WindowStyle Hidden"'
                # subprocess.run(cmd_kill, shell=True)

                # # หน่วงเวลาสั้นๆ ให้ระบบปิดโปรแกรมเสร็จเด็ดขาดก่อนลบไฟล์
                # import time
                # time.sleep(1)

                # # ลบไฟล์เก่าออกก่อนดาวน์โหลดใหม่ (ถ้ามีไฟล์อยู่)
                # if os.path.exists(MAIN_EXE):
                #     os.remove(MAIN_EXE)
                
                # 1. บังคับปิดแอปเก่าที่เปิดค้างอยู่ก่อน เพื่อปลดล็อกไฟล์ (สิทธิ์ปกติ ไม่เด้งเตือน)
                subprocess.run("taskkill /f /im main8.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                # หน่วงเวลาสั้นๆ 0.5 วินาที เพื่อให้ Windows ปลดล็อกไฟล์เสร็จเด็ดขาด
                import time
                time.sleep(0.5)

                # ดาวน์โหลดไฟล์ตัวแอปหลักมาเขียนทับโดยตรง (ไม่ต้องสร้างไฟล์ .bat)
                with requests.get(server_data["download_url"], stream=True) as r:
                    r.raise_for_status()
                    with open(MAIN_EXE, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                    # บันทึกไฟล์ข้อมูลเวอร์ชันใหม่ลงเครื่องคอมพิวเตอร์ด้วย
                    with open(LOCAL_JSON, "w") as f:
                        json.dump(server_data, f)
        except:
            pass # ถ้าเน็ตหลุด ให้ข้ามไปเปิดแอปหลักเท่าที่มีอยู่ในเครื่อง (Offline Mode)
        
        # โหลดเสร็จแล้ว สั่งเปิดแอปหลักทันที และปิดตัว Launcher ลง
        if os.path.exists(MAIN_EXE):
            subprocess.Popen([MAIN_EXE], shell=True)
        sys.exit()

    # สั่งให้ทำงานหลังจากหน้าต่าง UI แสดงผลขึ้นมาแล้ว 100 มิลลิวินาที
    wd.after(100, process_update)
    wd.mainloop()

if __name__ == "__main__":
    run_launcher()
