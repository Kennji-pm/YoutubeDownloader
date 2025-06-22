import os

class Header():
    def __init__(self):
        pass

    def _clear_screen(self):
        os.system("cls") if os.name == "nt" else os.system("clear")

    def _print_header(self, title: str):
        self._clear_screen()
        print("="*70)
        print(f"💾 YOUTUBE DOWNLOADER TOOLS V1 - {title.upper()} 💾".center(70))
        print("="*70)