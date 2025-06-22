from ..header import Header
from ..utils.config import Configure

class SettingScreen():
    def __init__(self):
        self.header = Header()
        self.configure = Configure()

    def initialize(self):
        while True:
            self.header._print_header("Cấu hình công cụ")
            print("[1] Configure Folders")
            print("[2] Configure Threading")

            choice = input("Enter your choice ('q' to back): ").strip()
            if choice == "1":
                Configure().configure_folders()
            elif choice == "2":
                Configure().configure_threading()
            elif choice == "q":
                break
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng thử lại.")
                input("\nNhấn Enter để tiếp tục...")


