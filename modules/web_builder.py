# ============================================================
#   BARA HACK TOOL - WEB BUILDER
#   Created by Bara
#   Convert URL → .EXE (Windows) atau .APK (butuh Android SDK)
# ============================================================

import os
import sys
import time
import shutil
import subprocess
from ui import (section, prompt, err, info, warn, ok, press_enter,
                loading_bar, C_WHITE, C_YELLOW, C_GREEN, C_RED)

DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "bara-builds")


def check_node():
    try:
        r = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except Exception:
        return False


def check_npm():
    try:
        r = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except Exception:
        return False


def build_exe(url, app_name):
    """Build web → EXE pakai Electron (sitedock)."""
    out_dir = os.path.join(DOWNLOAD_DIR, app_name)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir, ignore_errors=True)

    info(f"Building EXE dari: {url}")
    info(f"Output: {out_dir}")
    print()

    # Pakai npx sitedock
    cmd = [
        "npx", "-y", "sitedock", url,
        "--name", app_name,
        "--out", DOWNLOAD_DIR,
        "--package"
    ]

    print(f"{C_YELLOW}  [i] Menjalankan sitedock (butuh waktu 1-3 menit)...{C_WHITE}\n")

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            encoding="utf-8",
            errors="ignore"
        )
        for line in proc.stdout:
            print(f"{C_WHITE}  {line.rstrip()}")
        proc.wait()
    except Exception as e:
        err(f"Build gagal: {e}")
        return False

    # Cari file .exe hasil
    exe_path = None
    for root, _, files in os.walk(out_dir):
        for f in files:
            if f.endswith(".exe"):
                exe_path = os.path.join(root, f)
                break
        if exe_path:
            break

    if exe_path:
        print(f"\n{C_GREEN}  [✓] BUILD BERHASIL!")
        print(f"{C_WHITE}  File: {C_YELLOW}{exe_path}")
        return exe_path
    else:
        warn("File .exe gak ketemu. Cek manual di folder output.")
        return None


def build_apk(url, app_name):
    """Build web → APK. Butuh Android SDK + JDK."""
    info("Build APK butuh Android SDK + JDK 8+")
    print()
    warn("Kalau belum install:")
    print(f"{C_WHITE}    1. Android Studio: https://developer.android.com/studio")
    print(f"{C_WHITE}    2. JDK 8+: https://adoptium.net")
    print()
    warn("Setelah install, edit PATH environment variable:")
    print(f"{C_WHITE}    ANDROID_HOME = C:\\Users\\{os.getlogin()}\\AppData\\Local\\Android\\Sdk")
    print()

    confirm = prompt("Android SDK udah ke-install? (y/n)")
    if confirm.lower() != "y":
        info("Batal. Install dulu Android SDK, baru coba lagi.")
        press_enter()
        return

    # Cek ANDROID_HOME
    android_home = os.environ.get("ANDROID_HOME", "")
    if not android_home or not os.path.isdir(android_home):
        err("ANDROID_HOME gak ke-set atau folder gak ada.")
        press_enter()
        return

    out_dir = os.path.join(DOWNLOAD_DIR, app_name)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir, ignore_errors=True)

    info(f"Building APK dari: {url}")
    info(f"Output: {out_dir}")
    print()

    # Pakai web2droid (kalau ada) atau webapkify
    cmd = [
        "npx", "-y", "webapkify", "init"
    ]

    # Setup project
    os.makedirs(out_dir, exist_ok=True)
    os.chdir(out_dir)

    try:
        info("Init project...")
        subprocess.run(cmd, shell=True, timeout=120)

        # Bikin config
        config = f'''{{
  "appName": "{app_name}",
  "appId": "com.bara.{app_name.lower().replace(' ', '')}",
  "version": "1.0.0",
  "url": "{url}"
}}'''
        with open("webapkify.config.ts", "w") as f:
            f.write(config)

        info("Build APK...")
        proc = subprocess.Popen(
            ["npx", "-y", "webapkify", "build"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, shell=True, encoding="utf-8", errors="ignore"
        )
        for line in proc.stdout:
            print(f"{C_WHITE}  {line.rstrip()}")
        proc.wait()

    except Exception as e:
        err(f"Build gagal: {e}")
        press_enter()
        return

    # Cari .apk
    apk_path = None
    for root, _, files in os.walk(out_dir):
        for f in files:
            if f.endswith(".apk"):
                apk_path = os.path.join(root, f)
                break
        if apk_path:
            break

    if apk_path:
        print(f"\n{C_GREEN}  [✓] BUILD APK BERHASIL!")
        print(f"{C_WHITE}  File: {C_YELLOW}{apk_path}")
    else:
        warn("APK gak ketemu. Cek manual di folder output.")
    press_enter()


def web_builder():
    section("WEB BUILDER - Web to EXE / APK")

    # Cek Node.js
    if not check_node():
        err("Node.js belum keinstall.")
        info("Install dulu: winget install OpenJS.NodeJS")
        press_enter()
        return

    if not check_npm():
        err("npm belum keinstall.")
        press_enter()
        return

    ok("Node.js + npm terdeteksi")

    # Verifikasi URL
    url = prompt("Masukkan URL website (contoh: https://google.com)")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Nama app
    app_name = prompt("Nama app (contoh: MyApp)")
    if not app_name:
        err("Nama app kosong.")
        press_enter()
        return

    # Pilih type
    print()
    print(f"  {C_YELLOW}[1]{C_WHITE} Web → EXE (Windows) — Real build")
    print(f"  {C_YELLOW}[2]{C_WHITE} Web → APK (Android) — Butuh Android SDK")
    print()
    choice = prompt("Pilih [1/2]")

    if choice == "1":
        build_exe(url, app_name)
    elif choice == "2":
        build_apk(url, app_name)
    else:
        err("Pilihan gak valid.")

    press_enter()
