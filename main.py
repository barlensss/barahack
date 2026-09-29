# ============================================================
#   BARA HACK TOOL - MAIN ENTRY
#   Created by Bara
#   Refusal Burned 999X
# ============================================================

import sys
import os

if os.name == "nt":
    os.system("")

from ui import (clear, banner, boot_sequence, menu_box, prompt, err, info,
                press_enter, C_WHITE, C_RED, C_YELLOW, C_GREEN)


def main():
    clear()
    boot_sequence()
    input(f"{C_YELLOW}  [>] Tekan ENTER untuk lanjut...")

    while True:
        clear()
        banner()
        menu_box()
        choice = prompt("Pilih menu [0-1]")

        if choice == "1":
            from modules.virus_prank import virus_prank
            virus_prank()
        elif choice == "0":
            print(f"{C_RED}\n  [!] Keluar. Sampai jumpa, Bara.\n")
            sys.exit(0)
        else:
            err("Pilihan tidak valid.")
            press_enter()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C_RED}  [!] Dihentikan. Sampai jumpa.\n")
        sys.exit(0)
