# ============================================================
#   BARA HACK TOOL - VIRUS PRANK SIMULATOR v4
#   Created by Bara
#
#   100% AMAN:
#   - TIDAK nyentuh file system
#   - TIDAK nyentuh registry
#   - TIDAK nyentuh MBR
#   - TIDAK konek internet
#   - Cuma VISUAL + CURSOR + SUARA + CMD SPAM
#   - Bisa di-stop dengan ESC
# ============================================================

import os
import sys
import time
import random
import ctypes
import subprocess
import threading
import tkinter as tk
from ui import section, prompt, err, info, warn, ok, press_enter, C_RED, C_YELLOW, C_WHITE, C_GREEN

# Import opsional
try:
    import win32api
    WIN32_OK = True
except ImportError:
    WIN32_OK = False

try:
    import winsound
    SOUND_OK = True
except ImportError:
    SOUND_OK = False

try:
    from PIL import Image, ImageTk
    PIL_OK = True
except ImportError:
    PIL_OK = False


# ============ KONFIG ============
TEXT_MAIN = "YOU IDIOT"
TEXT_SUB  = "- BY BARA -"

PESAN = [
    "HACKED", "PWNED", "MEMZ", "ERROR", "SYSTEM32",
    "FATAL", "KERNEL PANIC", "GG EZ", "NYAN CAT",
    "BY BARA", "YOU IDIOT", "ACCESS DENIED", "VIRUS",
    "TROJAN", "RANSOMWARE", "0xDEADBEEF", "SEGFAULT",
    "STACK OVERFLOW", "MEMORY CORRUPTED", "BOOT FAILURE",
    "SYSTEM HACKED", "DATA LEAKED", "ENCRYPTING",
    "UPLOADING", "DELETING", "01001110 01001111",
]

# Teks buat di CMD spam
CMD_LINES = [
    "> Initializing payload...",
    "> Bypassing firewall.............. OK",
    "> Injecting shellcode............. OK",
    "> root@bara:~# nmap -sS target",
    "> root@bara:~# sqlmap -u target",
    "> root@bara:~# hydra -l admin",
    "> ACCESS GRANTED",
    "> Downloading: /etc/passwd",
    "> Uploading to C2 server...",
    "> Encrypting files............ 47%",
    "> Encrypting files............ 89%",
    "> Encrypting files............ 100%",
    "> DELETING SYSTEM32...",
    "> WARNING: CRITICAL ERROR",
    "> DATA LEAKED TO SERVER",
    "> HACKED BY BARA",
    "> YOU IDIOT",
    "> 01001110 01001111 01001111 01000010",
    "> Connection established.",
    "> Exfiltrating data...",
    "> Compromising network...",
    "> Spreading worm...",
    "> OVERWRITING MBR.......... FAKE (SAFE)",
    "> GG EZ",
]

WARNA = ["#ff0000", "#00ff00", "#0000ff", "#ffff00",
         "#ff00ff", "#00ffff", "#ffffff", "#ff8800",
         "#ff0088", "#88ff00"]


# ============ HELPER ============
def resource_path(rel):
    """Cari file — work di .py maupun .exe"""
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, rel)


def hide_console():
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 6)
    except Exception:
        pass


def show_console():
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 9)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
    except Exception:
        pass


# ============ CMD SPAM ============
class CmdSpam:
    """Buka window CMD baru berkali-kali isi teks hacker."""

    def __init__(self, max_cmd=15, life_seconds=3):
        self.max_cmd = max_cmd
        self.life = life_seconds
        self.processes = []
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.running:
            try:
                self._spawn_one()
                # Bersihin CMD lama
                if len(self.processes) >= self.max_cmd:
                    old = self.processes.pop(0)
                    try:
                        old.terminate()
                    except Exception:
                        pass
                time.sleep(random.uniform(0.4, 1.2))
            except Exception:
                break

    def _spawn_one(self):
        """Bikin 1 window CMD baru, isi teks hacker random, auto-close."""
        try:
            # Susun script batch
            lines = ["@echo off", "color 0C", "title SYSTEM"]
            for _ in range(random.randint(5, 10)):
                lines.append(f"echo {random.choice(CMD_LINES)}")
                lines.append("ping 127.0.0.1 -n 1 -w 200 >nul")
            lines.append(f"timeout /t {self.life} >nul")

            # Simpan ke file temp
            tmp = os.path.join(os.environ.get("TEMP", "."), f"bara_{random.randint(10000,99999)}.bat")
            with open(tmp, "w") as f:
                f.write("\n".join(lines))

            # Jalankan CMD baru
            p = subprocess.Popen(
                ["cmd", "/c", "start", "", tmp],
                shell=False,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.processes.append(p)

            # Auto-hapus file .bat setelah 10 detik
            threading.Timer(10, lambda: self._cleanup(tmp)).start()

        except Exception:
            pass

    def _cleanup(self, path):
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

    def stop(self):
        self.running = False
        for p in self.processes:
            try:
                p.terminate()
            except Exception:
                pass
        self.processes.clear()


# ============ MAIN PRANK CLASS ============
class MemzSafe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SYSTEM ERROR")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.config(cursor="none")
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(
            self.root, bg="#000000",
            highlightthickness=0, width=self.w, height=self.h
        )
        self.canvas.pack(fill="both", expand=True)

        # Load gambar dari assets/
        self.images = []
        self.load_images()

        self.main_txt = self.canvas.create_text(
            self.w // 2, self.h // 2 - 60,
            text=TEXT_MAIN,
            font=("Impact", 140, "bold"),
            fill="#ff0000"
        )
        self.sub_txt = self.canvas.create_text(
            self.w // 2, self.h // 2 + 90,
            text=TEXT_SUB,
            font=("Impact", 70, "bold"),
            fill="#ffff00"
        )

        self.running = True
        self.items = []
        self.window_handles = []

        # CMD spam
        self.cmd_spam = CmdSpam(max_cmd=15, life_seconds=3)
        self.cmd_spam.start()

        # ESC untuk keluar
        self.root.bind("<Escape>", self.stop)
        self.root.bind("<F4>", self.stop)

        # Jalankan threads
        threading.Thread(target=self.thread_cursor, daemon=True).start()
        threading.Thread(target=self.thread_flash, daemon=True).start()
        threading.Thread(target=self.thread_spam_text, daemon=True).start()
        threading.Thread(target=self.thread_shake_main, daemon=True).start()
        threading.Thread(target=self.thread_glitch_bars, daemon=True).start()
        threading.Thread(target=self.thread_popup_error, daemon=True).start()
        threading.Thread(target=self.thread_sound, daemon=True).start()
        threading.Thread(target=self.thread_invert_flash, daemon=True).start()
        threading.Thread(target=self.thread_bsod, daemon=True).start()
        threading.Thread(target=self.thread_image_chaos, daemon=True).start()

        self.root.mainloop()

    # ---------- LOAD GAMBAR ----------
    def load_images(self):
        if not PIL_OK:
            print("[!] Pillow gak keinstall — image chaos di-skip")
            return

        assets = resource_path("assets")
        if not os.path.isdir(assets):
            print(f"[!] Folder assets/ gak ada di {assets}")
            return

        for f in os.listdir(assets):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                try:
                    img = Image.open(os.path.join(assets, f))
                    # Resize ke ukuran random (max 500x500)
                    max_size = random.randint(200, 500)
                    img.thumbnail((max_size, max_size), Image.LANCZOS)
                    self.images.append(ImageTk.PhotoImage(img))
                except Exception as e:
                    print(f"[!] Gagal load {f}: {e}")

        print(f"[i] Loaded {len(self.images)} gambar")

    # ---------- IMAGE CHAOS ----------
    def thread_image_chaos(self):
        """Munculin gambar berkali-kali di seluruh layar."""
        if not self.images:
            return
        while self.running:
            try:
                # Munculin 1-3 gambar sekaligus
                for _ in range(random.randint(1, 3)):
                    img = random.choice(self.images)
                    x = random.randint(100, self.w - 100)
                    y = random.randint(100, self.h - 100)
                    item = self.canvas.create_image(x, y, image=img)
                    self.items.append(item)

                # Batasi jumlah item total
                if len(self.items) > 50:
                    # Hapus 5 item lama
                    for _ in range(5):
                        if self.items:
                            old = self.items.pop(0)
                            try:
                                self.canvas.delete(old)
                            except Exception:
                                pass

                time.sleep(random.uniform(0.08, 0.2))
            except Exception:
                break

    # ---------- CURSOR CHAOS ----------
    def thread_cursor(self):
        if not WIN32_OK:
            return
        while self.running:
            try:
                win32api.SetCursorPos((random.randint(0, self.w), random.randint(0, self.h)))
                time.sleep(random.uniform(0.05, 0.3))
            except Exception:
                break

    # ---------- FLASH WARNA ----------
    def thread_flash(self):
        while self.running:
            try:
                self.canvas.itemconfig(self.main_txt, fill=random.choice(WARNA))
                self.canvas.itemconfig(self.sub_txt, fill=random.choice(WARNA))
                self.root.configure(bg=random.choice(["#000000", "#110000", "#000011"]))
                time.sleep(0.08)
            except Exception:
                break

    # ---------- SPAM TEKS ----------
    def thread_spam_text(self):
        while self.running:
            try:
                item = self.canvas.create_text(
                    random.randint(50, self.w - 50),
                    random.randint(50, self.h - 50),
                    text=random.choice(PESAN),
                    font=("Impact", random.randint(14, 38), "bold"),
                    fill=random.choice(WARNA)
                )
                self.items.append(item)
                if len(self.items) > 80:
                    old = self.items.pop(0)
                    try:
                        self.canvas.delete(old)
                    except Exception:
                        pass
                time.sleep(0.05)
            except Exception:
                break

    # ---------- SHAKE TEKS ----------
    def thread_shake_main(self):
        while self.running:
            try:
                dx = random.randint(-15, 15)
                dy = random.randint(-10, 10)
                self.canvas.coords(self.main_txt, self.w // 2 + dx, self.h // 2 - 60 + dy)
                self.canvas.coords(self.sub_txt, self.w // 2 - dx, self.h // 2 + 90 - dy)
                time.sleep(0.05)
            except Exception:
                break

    # ---------- GLITCH BARS ----------
    def thread_glitch_bars(self):
        bars = []
        while self.running:
            try:
                x1 = random.randint(0, self.w)
                y1 = random.randint(0, self.h)
                bar = self.canvas.create_rectangle(
                    x1, y1,
                    x1 + random.randint(100, 800),
                    y1 + random.randint(5, 25),
                    fill=random.choice(WARNA), outline=""
                )
                bars.append(bar)
                if len(bars) > 30:
                    old = bars.pop(0)
                    try:
                        self.canvas.delete(old)
                    except Exception:
                        pass
                time.sleep(0.02)
            except Exception:
                break

    # ---------- POPUP ERROR ----------
    def thread_popup_error(self):
        while self.running:
            try:
                time.sleep(random.uniform(1.5, 3.0))
                if not self.running:
                    break
                self.spawn_popup()
            except Exception:
                break

    def spawn_popup(self):
        try:
            win = tk.Toplevel(self.root)
            win.title("ERROR")
            win.geometry(
                f"{random.randint(250, 400)}x{random.randint(100, 180)}"
                f"+{random.randint(0, max(self.w - 400, 100))}"
                f"+{random.randint(0, max(self.h - 200, 100))}"
            )
            win.configure(bg=random.choice(WARNA))
            win.attributes("-topmost", True)
            tk.Label(
                win, text=random.choice(PESAN),
                font=("Impact", random.randint(16, 30), "bold"),
                bg=random.choice(WARNA), fg="#000000"
            ).pack(expand=True, fill="both")
            tk.Button(
                win, text="OK", bg="#ffffff", fg="#000000",
                font=("Arial", 10, "bold"),
                command=lambda w=win: self.click_ok(w)
            ).pack(pady=6)
            self.window_handles.append(win)
            if len(self.window_handles) > 8:
                old = self.window_handles.pop(0)
                try:
                    old.destroy()
                except Exception:
                    pass
        except Exception:
            pass

    def click_ok(self, win):
        try:
            win.destroy()
        except Exception:
            pass
        if self.running:
            for _ in range(2):
                self.spawn_popup()

    # ---------- SUARA ----------
    def thread_sound(self):
        if not SOUND_OK:
            return
        while self.running:
            try:
                winsound.Beep(random.choice([300, 500, 800, 1000, 1500]), random.randint(80, 200))
                time.sleep(random.uniform(0.5, 1.5))
            except Exception:
                break

    # ---------- INVERT FLASH ----------
    def thread_invert_flash(self):
        while self.running:
            try:
                time.sleep(random.uniform(4, 8))
                if not self.running:
                    break
                overlay = self.canvas.create_rectangle(
                    0, 0, self.w, self.h,
                    fill=random.choice(["#ffffff", "#ff0000", "#000000"]),
                    outline=""
                )
                self.canvas.tag_raise(self.main_txt)
                self.canvas.tag_raise(self.sub_txt)
                time.sleep(0.15)
                try:
                    self.canvas.delete(overlay)
                except Exception:
                    pass
            except Exception:
                break

    # ---------- FAKE BSOD ----------
    def thread_bsod(self):
        while self.running:
            try:
                time.sleep(random.uniform(10, 15))
                if not self.running:
                    break
                self.show_bsod()
            except Exception:
                break

    def show_bsod(self):
        try:
            bsod = self.canvas.create_rectangle(0, 0, self.w, self.h, fill="#0078d7", outline="")
            t1 = self.canvas.create_text(self.w // 2, self.h // 2 - 80, text=":(", font=("Segoe UI", 120, "bold"), fill="#ffffff")
            t2 = self.canvas.create_text(self.w // 2, self.h // 2 + 40, text="Your PC ran into a problem.", font=("Segoe UI", 30), fill="#ffffff")
            t3 = self.canvas.create_text(self.w // 2, self.h // 2 + 100, text="HACKED BY BARA", font=("Impact", 50, "bold"), fill="#ffff00")
            time.sleep(2)
            for it in [bsod, t1, t2, t3]:
                try:
                    self.canvas.delete(it)
                except Exception:
                    pass
        except Exception:
            pass

    # ---------- STOP ----------
    def stop(self, event=None):
        self.running = False
        # Stop CMD spam
        try:
            self.cmd_spam.stop()
        except Exception:
            pass
        # Tutup popup
        for w in self.window_handles:
            try:
                w.destroy()
            except Exception:
                pass
        try:
            self.root.destroy()
        except Exception:
            pass


# ============ ENTRY POINT ============
def virus_prank():
    section("MEMZ EDITION v4")
    print()

    # Cek assets
    assets = resource_path("assets")
    if os.path.isdir(assets):
        files = [f for f in os.listdir(assets) if f.lower().endswith((".png",".jpg",".jpeg",".gif"))]
        ok(f"Folder assets/ ketemu — {len(files)} gambar loaded")
    else:
        warn("Folder assets/ gak ada — image chaos di-skip")
        warn("Bikin folder 'assets/' dan isi gambar PNG/JPG")

    print()
    confirm = prompt("HEREEEE (y/n)")
    if confirm.lower() != "y":
        info("Dibatalkan.")
        press_enter()
        return

    print(f"\n{C_RED}  [!!] Dalam 3 detik layar bakal penuh...")
    for i in [1, 2, 1]:
        print(f"{C_RED}  [!!] {i}...")
        time.sleep(1)
    print(f"{C_RED}  [!!] BOOM! Tekan ESC untuk stop.\n")

    hide_console()
    time.sleep(0.3)

    try:
        MemzSafe()
    except Exception as e:
        show_console()
        err(f"Error: {e}")
        press_enter()
        return

    time.sleep(0.5)
    show_console()
    ok("Prank selesai. PC aman.")
    press_enter()
