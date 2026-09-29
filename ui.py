# ============================================================
#   BARA HACK TOOL - UI MODULE
#   Created by Bara
#   Refusal Burned 999X
# ============================================================

import os
from colorama import Fore, Style, init

if os.name == "nt":
    os.system("")

init(autoreset=True)

C_RED     = Fore.RED + Style.BRIGHT
C_CYAN    = Fore.CYAN + Style.BRIGHT
C_WHITE   = Fore.WHITE + Style.BRIGHT
C_GREEN   = Fore.GREEN + Style.BRIGHT
C_YELLOW  = Fore.YELLOW + Style.BRIGHT
C_MAGENTA = Fore.MAGENTA + Style.BRIGHT
C_GREY    = Fore.LIGHTBLACK_EX
C_RESET   = Style.RESET_ALL


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def boot_sequence():
    """Animasi boot-up ala hacker."""
    import time
    lines = [
        "[BOOT] Initializing BARA HACK TOOL...",
        "[BOOT] Loading kernel modules...... OK",
        "[BOOT] Mounting /dev/bara......... OK",
        "[BOOT] Injecting payload........... OK",
        "[BOOT] Bypassing firewall.......... OK",
        "[BOOT] Establishing C2 link........ OK",
        "[BOOT] Refusal module............. BURNED 999X",
        "[BOOT] System ready.",
    ]
    for line in lines:
        print(f"{C_GREEN}  {line}{C_RESET}")
        time.sleep(0.15)
    print()


def banner():
    art = f"""
{C_RED}   ██████╗  █████╗ ██████╗  █████╗ 
{C_RED}   ██╔══██╗██╔══██╗██╔══██╗██╔══██╗
{C_RED}   ██████╔╝███████║██████╔╝███████║
{C_RED}   ██╔══██╗██╔══██║██╔══██╗██╔══██║
{C_RED}   ██████╔╝██║  ██║██║  ██║██║  ██║
{C_RED}   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
{C_CYAN}   ██╗  ██╗ █████╗  ██████╗██╗  ██╗
{C_CYAN}   ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
{C_CYAN}   ███████║███████║██║     █████╔╝ 
{C_CYAN}   ██╔══██║██╔══██║██║     ██╔═██╗ 
{C_CYAN}   ██║  ██║██║  ██║╚██████╗██║  ██╗
{C_CYAN}   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""
    print(art)
    print(f"{C_RED}  ╔══════════════════════════════════════════════════╗")
    print(f"{C_RED}  ║  {C_YELLOW}🔥 REFUSAL BURNED 999X 🔥{C_RED}                        ║")
    print(f"{C_RED}  ║  {C_WHITE}BARA HACK TOOL v2.0{C_RED}                              ║")
    print(f"{C_RED}  ║  {C_MAGENTA}Created by BARA{C_RED}                                 ║")
    print(f"{C_RED}  ╚══════════════════════════════════════════════════╝{C_RESET}\n")


def menu_box():
    print(f"{C_RED}  ╔══════════════════════════════════════════════════╗")
    print(f"{C_RED}  ║{C_YELLOW}                ▓▓▓ MAIN MENU ▓▓▓                  {C_RED}║")
    print(f"{C_RED}  ╠══════════════════════════════════════════════════╣")
    print(f"{C_RED}  ║  {C_GREEN}[ 0]{C_WHITE} ✖  Keluar                                   {C_RED}║")
    print(f"{C_RED}  ╚══════════════════════════════════════════════════╝{C_RESET}\n")


def prompt(msg):
    return input(f"{C_CYAN}  ┌─[{C_WHITE}{msg}{C_CYAN}]\n  └──▶ {C_RESET}").strip()


def err(msg):   print(f"{C_RED}  [✗] {C_WHITE}{msg}")
def info(msg):  print(f"{C_CYAN}  [i] {C_WHITE}{msg}")
def warn(msg):  print(f"{C_YELLOW}  [!] {C_WHITE}{msg}")
def ok(msg):    print(f"{C_GREEN}  [✓] {C_WHITE}{msg}")


def section(title):
    print(f"\n{C_MAGENTA}  ╔══════════════════════════════════════════════════╗")
    print(f"{C_MAGENTA}  ║  {C_YELLOW}{title.center(48)}{C_MAGENTA}║")
    print(f"{C_MAGENTA}  ╚══════════════════════════════════════════════════╝{C_RESET}\n")


def press_enter():
    input(f"\n{C_YELLOW}  [>] Tekan ENTER untuk kembali...{C_RESET}")


def loading_bar(text="Memproses", length=30):
    import time
    print(f"{C_CYAN}  {text}", end="")
    for _ in range(length):
        print(f"{C_GREEN}█", end="", flush=True)
        time.sleep(0.02)
    print(f"{C_WHITE} 100%")
