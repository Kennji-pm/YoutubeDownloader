import time

from tqdm import tqdm
from pytubefix import YouTube, Search, streams
from pytubefix.cli import on_progress
from pytubefix.exceptions import VideoUnavailable, VideoPrivate, VideoRegionBlocked, LoginRequired

from ..header import Header
from ..utils.config import Configure
from ..misc.convert import convert_seconds, convert_filesize

class DownloadService:
    def __init__(self):
        self.header = Header()
        self.configure = Configure()

        self.video_folder = self.configure.video_folder
        self.audio_folder = self.configure.audio_folder

        self.progress_bar = None
        self.bytes_downloaded_in_current_file = 0

    def _on_progress(self, stream: streams.Stream, chunk: bytes, bytes_remaining: int):
        # Calculate bytes just downloaded in this chunk
        current_bytes_downloaded = stream.filesize - bytes_remaining
        newly_downloaded_bytes = current_bytes_downloaded - self.bytes_downloaded_in_current_file

        if self.progress_bar:
            self.progress_bar.update(newly_downloaded_bytes)

        # Update the tracker for the current file's progress
        self.bytes_downloaded_in_current_file = current_bytes_downloaded

    def download_video_audio_from_url(self):
        """
        Download a video from a given URL and save it to the specified output path.
        """
        while True:
            self.header._print_header("Download video/audio from URL")
            print(f"📂 Folders:")
            print(f"   🎵Audio: {self.configure.audio_folder}")
            print(f"   🎥Video: {self.configure.video_folder}")
            print("-" * 70)
            print("[q] To back")
            print("=" * 70)
            try:
                url_input = input(">>> Nhập URL: ").strip()
                if url_input == "q":
                    break

                yt = YouTube(url=url_input, on_progress_callback=self._on_progress)
                print("\n"+"-" * 70)
                print(f"Tiêu đề: {yt.title}")
                print(f"Tác giả: {yt.author}")
                print(f"Lượt xem: {yt.views:,}")
                print(f"Thời lượng: {convert_seconds(yt.length)}")
                print("-" * 70)
                output_type = ""
                while output_type not in ["video", "audio"]:
                    choice = input(f"Chọn loại tải xuống (video/audio): ").lower().strip()
                    if choice in ["video", "v"]:
                        output_type = "video"
                    elif choice in ["audio", "a"]:
                        output_type = "audio"
                    else:
                        print(f"⚠️ Lựa chọn không hợp lệ. Vui lòng nhập 'video' hoặc 'audio'.")
                if output_type == "video":
                    ds = yt.streams.get_highest_resolution()
                    output_path = self.video_folder
                else:
                    ds = yt.streams.get_audio_only()
                    output_path = self.audio_folder

                self.header._print_header("Bắt đầu tải xuống...")
                print(f"Tên tệp: {ds.default_filename}")
                print(f"Kích thước: {convert_filesize(ds.filesize)}")
                print(f"Lưu tại: {output_path}/{ds.default_filename}")
                print("=" * 70)
                self.progress_bar = None
                try:
                    self.progress_bar = tqdm(
                        total=ds.filesize,
                        unit='B',
                        unit_scale=True,
                        desc=f"Đang tải...",
                        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
                    )
                    ds.download(output_path=output_path)
                    remaining_bytes = self.progress_bar.total - self.progress_bar.n
                    if remaining_bytes > 0:
                        self.progress_bar.update(remaining_bytes)
                    self.progress_bar.close()
                    self.progress_bar = None
                finally:
                    # Đảm bảo thanh progress bar luôn được đóng
                    if self.progress_bar:
                        self.progress_bar.close()
                        self.progress_bar = None
                print("\n✅ Tải xuống thành công!")
                input("\nNhấn Enter để tiếp tục...")
            except Exception as e:
                print(f"❌ Đã xảy ra lỗi không xác định: {str(e)}")
                input("\nNhấn Enter để tiếp tục...")

            except (VideoUnavailable, VideoPrivate, VideoRegionBlocked) as e:
                print(f"❌ Lỗi Video: {e}")
                input("\nNhấn Enter để tiếp tục...")
            except LoginRequired as e:
                print(f"❌ Lỗi đăng nhập: {e}")
                input("\nNhấn Enter để tiếp tục...")

    def download_from_keyword(self):
        """
        Download a video from a given keyword and save it to the specified output path.
        """
        video_id_list = []
        while True:
            self.header._print_header("Download video/audio from keyword")
            print(f"📂 Folders:")
            print(f"   🎵Audio: {self.configure.audio_folder}")
            print(f"   🎥Video: {self.configure.video_folder}")
            print("-" * 70)
            print("[q] To back")
            print("=" * 70)
            try:
                keyword = input(">>> Nhập Keyword: ")
                if keyword == "q":
                    break

                results = Search(query=keyword)
                print("\nSearching...")
                print(""+"-" * 70)
                for i, result in enumerate(results.videos):
                    video_id_list.append([
                        f"https://www.youtube.com/watch?v={result.video_id}",
                        result.title
                    ])
                    print(f"|     ID: {result.video_id}")
                    print(f"|     Tiêu đề: {result.title}")
                    print(f"[{i+1}]  Tác giả: {result.author}")
                    print(f"|     Lượt xem: {result.views:,}")
                    print(f"|     Thời lượng: {convert_seconds(result.length)}")
                    print("-" * 70)


                print("\n💡 Chọn nhiều lựa chọn bằng cách nhập các số, cách nhau bởi dấu phẩy (,)")
                print("    Ví dụ: 1,3,5 sẽ chọn lựa chọn 1, 3 và 5")
                print("    Nhập 'all' để chọn tất cả các lựa chọn")
                
                choice = input("\n🔢 Nhập lựa chọn của bạn (hoặc 'q' để quay lại): ")

                if choice.lower() == 'q':
                    return
                
                option_to_choice = []
                
                if choice.lower() == 'all':
                    option_to_choice = video_id_list
                else:
                    # Xử lý khi người dùng nhập danh sách số
                    selected_indices = [int(idx.strip()) - 1 for idx in choice.split(',')]
                    
                    for idx in selected_indices:
                        if 0 <= idx < len(video_id_list):
                            option_to_choice.append(video_id_list[idx])
                        else:
                            print(f"⚠️ Bỏ qua số không hợp lệ: {idx+1}")
                
                if not option_to_choice:
                    print("❌ Không có lựa chọn nào được chọn hợp lệ")
                    input("\nNhấn Enter để tiếp tục...")
                    return
                
                # Hiển thị danh sách lựa chọn
                print("\n✅ Các lựa chọn sẽ tải xuống:")
                for i, (link, title) in enumerate(option_to_choice):
                    print(f" - {title}")
                input("\nNhấn Enter để tiếp tục...")
                self.header._print_header(f"Tải Xuống ({len(option_to_choice)} lựa chọn)")
                print(f"📂 Folders:")
                print(f"   🎵Audio: {self.configure.audio_folder}")
                print(f"   🎥Video: {self.configure.video_folder}")
                print("=" * 70)
                for i, (link, title) in enumerate(option_to_choice):
                    print(f"[{i+1}] - {title}")
                type_download = input("Chọn loại tải xuống (video/audio): ").strip()
                while type_download not in ["video", "audio"]:
                    choice = input(f"Chọn loại tải xuống (video/audio): ").lower().strip()
                    if choice in ["video", "v"]:
                        type_download = "video"
                    elif choice in ["audio", "a"]:
                        type_download = "audio"
                    else:
                        print(f"⚠️ Lựa chọn không hợp lệ. Vui lòng nhập 'video' hoặc 'audio'.")
                start_time = time.time()
                total_size = 0
                for link, title in option_to_choice:
                    yt = YouTube(url=link)
                    if type_download == "video":
                        ds = yt.streams.get_highest_resolution()
                    else:
                        ds = yt.streams.get_audio_only()
                    total_size += ds.filesize

                with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Tổng ({len(option_to_choice)} lựa chọn)") as pbar:
                    for i, (link, title) in enumerate(option_to_choice):
                        yt = YouTube(url=link, on_progress_callback=self._on_progress)
                        if type_download == "video":
                            ds = yt.streams.get_highest_resolution()
                            output_path = self.video_folder
                        else:
                            ds = yt.streams.get_audio_only()
                            output_path = self.audio_folder

                        try:
                            self.bytes_downloaded_in_current_file = 0
                            ds.download(output_path=output_path, filename=title+".mp4" if type_download == "video" else title+".mp3")
                            pbar.update(ds.filesize)
                            time.sleep(1)
                        except Exception as e:
                            print(f"❌ Lỗi khi tải {title}: {str(e)}")
                        finally:
                            pass # No need to close the progress bar here
                self.progress_bar = None
                end_time = time.time()
                print(f"Thời gian tải xuống: {convert_seconds(end_time - start_time)}")
                input("\nNhấn Enter để tiếp tục...")

            except Exception as e:
                print(f"❌ Đã xảy ra lỗi không xác định: {str(e)}")
                input("\nNhấn Enter để tiếp tục...")

            except (VideoUnavailable, VideoPrivate, VideoRegionBlocked) as e:
                print(f"❌ Lỗi Video: {e}")
                input("\nNhấn Enter để tiếp tục...")
            except LoginRequired as e:
                print(f"❌ Lỗi đăng nhập: {e}")
                input("\nNhấn Enter để tiếp tục...")