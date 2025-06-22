import os
import json
from dotenv import load_dotenv
from ..header import Header

class Configure():
    def __init__(self):
        self.project_root = "youtube_downloader_projects"
        self.audio_folder = os.path.join(self.project_root, "audio")
        self.video_folder = os.path.join(self.project_root, "video")
        self.thumbnail_folder = os.path.join(self.project_root, "thumbnail")
        self.config_file = os.path.join(self.project_root, "config.json")
        self.max_workers = 4

        self.filter_options = {
            'upload_date': 'Today',
            'type': 'Video',
            'duration': 'Under 4 minutes',
            'features': ['4K', 'Creative Commons'],
            'sort_by': 'Upload date'
        }

        load_dotenv()

        os.makedirs(self.audio_folder, exist_ok=True)
        os.makedirs(self.video_folder, exist_ok=True)
        os.makedirs(self.thumbnail_folder, exist_ok=True)
        
        # Tải cấu hình nếu có
        self.load_config()

        self.header = Header()

    def _max_workers(self):
        return self.max_workers
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    if "max_workers" in config:
                        self.max_workers = config["max_workers"]
                    if "folders" in config:
                        self.audio_folder = config["folders"].get("audio", self.audio_folder)
                        self.video_folder = config["folders"].get("video", self.video_folder)
                        self.thumbnail_folder = config["folders"].get("thumbnail", self.thumbnail_folder)
                    if "filters" in config:
                        self.filter_options = config["filters"]

        except Exception as e:
            print(f"⚠️ Không thể đọc file cấu hình: {str(e)}")
    
    def save_config(self):
        """Lưu cấu hình vào file config.json"""
        try:
            config = {
                'max_workers': self.max_workers,
                'folders': {
                    'audio': self.audio_folder,
                    'video': self.video_folder,
                    'thumbnail': self.thumbnail_folder
                },
                'filters': self.filter_options
            }
            
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
            print(f"✅ Đã lưu cấu hình vào {self.config_file}")
        except Exception as e:
            print(f"⚠️ Không thể lưu file cấu hình: {str(e)}")

    def configure_threading(self):
        """Cấu hình số luồng tối đa"""
        self.header._print_header("Cấu hình luồng")
        print(f"Số luồng hiện tại: {self.max_workers}")
        
        try:
            new_workers = input(f"Nhập số luồng mới (1-16, mặc định: {self.max_workers}): ").strip()
            if new_workers:
                new_workers = int(new_workers)
                if 1 <= new_workers <= 16:
                    self.max_workers = new_workers
                    print(f"✅ Đã cập nhật số luồng thành: {self.max_workers}")
                else:
                    print("⚠️ Số luồng phải từ 1-16, giữ nguyên giá trị hiện tại.")
            else:
                print(f"✅ Giữ nguyên số luồng: {self.max_workers}")
        except ValueError:
            print("⚠️ Giá trị không hợp lệ, giữ nguyên số luồng hiện tại.")
        
        # Lưu cấu hình sau khi thay đổi
        self.save_config()
        input("\nNhấn Enter để tiếp tục...")

    def configure_folders(self):
        """Cấu hình thư mục lưu trữ"""
        while True:
            self.header._print_header("Cấu hình thư mục")
            print(f"Thư mục lưu trữ hiện tại:")
            print(f"    🎵Audio: {self.audio_folder}")
            print(f"    🎥Video: {self.video_folder}")
            print(f"    🖼️Thumbnail: {self.thumbnail_folder}")
            print("=" * 70)
            print(" [1] Change Audio folder")
            print(" [2] Change Video folder")
            print(" [3] Change Thumbnail folder")
            print(" [0] Back")
            print("=" * 70)
            try:
                choice = input("Enter your option: ").strip()
                if choice == "1":
                    new_audio_folder = input(f"Nhập thư mục mới (mặc định: {self.audio_folder}): ").strip()
                    if new_audio_folder:
                        self.audio_folder = new_audio_folder
                        os.makedirs(self.audio_folder, exist_ok=True)
                        print(f"✅ Đã cập nhật thư mục lưu trữ audio thành: {self.audio_folder}")
                        input("\nNhấn Enter để tiếp tục...")
                    else:
                        print(f"✅ Giữ nguyên thư mục lưu trữ audio: {self.audio_folder}")
                        input("\nNhấn Enter để tiếp tục...")
                elif choice == "2":
                    new_video_folder = input(f"Nhập thư mục mới (mặc định: {self.video_folder}): ").strip()
                    if new_video_folder:
                        self.video_folder = new_video_folder
                        os.makedirs(self.video_folder, exist_ok=True)
                        print(f"✅ Đã cập nhật thư mục lưu trữ video thành: {self.video_folder}")
                        input("\nNhấn Enter để tiếp tục...")
                    else:
                        print(f"✅ Giữ nguyên thư mục lưu trữ video: {self.video_folder}")
                        input("\nNhấn Enter để tiếp tục...")
                elif choice == "3":
                    new_thumbnail_folder = input(f"Nhập thư mục mới (mặc định: {self.thumbnail_folder}): ").strip()
                    if new_thumbnail_folder:
                        self.thumbnail_folder = new_thumbnail_folder
                        os.makedirs(self.thumbnail_folder, exist_ok=True)
                        print(f"✅ Đã cập nhật thư mục lưu trữ thumbnail thành: {self.thumbnail_folder}")
                        input("\nNhấn Enter để tiếp tục...")
                    else:
                        print(f"✅ Giữ nguyên thư mục lưu trữ thumbnail: {self.thumbnail_folder}")
                        input("\nNhấn Enter để tiếp tục...")
                elif choice == "0":
                    break
                else:
                    print("⚠️ Lựa chọn không hợp lệ. Vui lòng thử lại.")
                    input("\nNhấn Enter để tiếp tục...")

                # Lưu cấu hình sau khi thay đổi
                self.save_config()

            except Exception as e:
                print(f"⚠️ Lỗi: {str(e)}")
                input("\nNhấn Enter để tiếp tục...")
                break