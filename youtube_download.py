import traceback
from core.utils.config import Configure
from core.header import Header
from core.screens.settings import SettingScreen
from core.services.download import DownloadService

class YoutubeDownloaderScreen():
    def __init__(self):
        self.configure = Configure()
        self.header = Header()
        self.download_service = DownloadService()

    def main(self):
        while True:
            self.header._print_header("Main screen")
            print(" [1] Download video/audio from URL")
            print(" [2] Download playlist from URL")
            print(" [3] Download from keyword")
            print("-"*70)
            print(" [4] Settings")
            print(" [0] Exit")
            print("=" * 70)
            print(f" 👤 Cấu hình hiện tại:")
            print(f"    🧵 Số luồng: {self.configure.max_workers}")
            print(f"    🔑 API:")
            print(f"    📂 Folders:")
            print(f"        🎵Audio: {self.configure.audio_folder}")
            print(f"        🎥Video: {self.configure.video_folder}")
            print(f"        🖼️Thumbnail: {self.configure.thumbnail_folder}")
            print("=" * 70)
            choice = input("Enter your option: ").strip()
            if choice == "1":
                self.download_service.download_video_audio_from_url()
            elif choice == "2":
                self.download_playlist()
            elif choice == "3":
                self.download_service.download_from_keyword()
            elif choice == "4":
                SettingScreen().initialize()
            elif choice == "0":
                self.header._clear_screen()
                print("\n🛑 Thoát chương trình...")
                print("👋 Cảm ơn đã sử dụng công cụ!")
                return
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng thử lại.")
                input("\nNhấn Enter để tiếp tục...")

    def run(self):
        try:
            self.header._print_header("Starting...")
            self.main()
        except KeyboardInterrupt:
            print("\n\n🛑 Chương trình bị ngắt bởi người dùng...")
            print("👋 Cảm ơn đã sử dụng công cụ!")
        except Exception as e:
            print(f"\n❌ Đã xảy ra lỗi không mong muốn: {str(e)}")
            traceback.print_exc()
            print("Vui lòng báo lỗi này cho nhà phát triển nếu cần thiết.")
            input("\nNhấn Enter để thoát.")
        finally:
            print("\nĐóng chương trình.")

if __name__ == "__main__":
    translator = YoutubeDownloaderScreen()
    translator.run()