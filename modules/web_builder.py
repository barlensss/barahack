# ============================================================
#   BARA HACK TOOL - WEB BUILDER v2
#   Created by Bara
#   Convert URL → .EXE (Windows) atau .APK (Android)
#   Fix: Windows npm.cmd detection
# ============================================================

import os
import sys
import time
import shutil
import subprocess
from ui import (section, prompt, err, info, warn, ok, press_enter,
                loading_bar, C_WHITE, C_YELLOW, C_GREEN, C_RED)

DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "bara-builds")


# ============ DETECT NODE / NPM (WINDOWS-AWARE) ============
def run_cmd(cmd, timeout=10):
    """Jalanin perintah dengan shell=True — work di Windows."""
    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=True,           # PENTING: biar npm.cmd ke-detect
            encoding="utf-8",
            errors="ignore"
        )
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, str(e)


def check_node():
    code, out = run_cmd("node --version")
    if code == 0 and out.strip().startswith("v"):
        return out.strip()
    return None


def check_npm():
    # Di Windows, npm itu npm.cmd — pakai shell=True biar ke-detect
    code, out = run_cmd("npm --version")
    if code == 0 and out.strip():
        return out.strip()
    return None


def check_npx():
    code, out = run_cmd("npx --version")
    if code == 0 and out.strip():
        return out.strip()
    return None


# ============ BUILD EXE ============
def build_exe(url, app_name):
    out_dir = os.path.join(DOWNLOAD_DIR, app_name)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir, ignore_errors=True)

    info(f"Building EXE dari: {url}")
    info(f"Output: {out_dir}")
    print()
    print(f"{C_YELLOW}  [i] Menjalankan sitedock (butuh waktu 1-3 menit)...{C_WHITE}\n")

    # Pakai shell=True biar npm.cmd / npx.cmd ke-detect
    cmd = f'npx -y sitedock "{url}" --name "{app_name}" --out "{DOWNLOAD_DIR}" --package'

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,           # PENTING
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


# ============ BUILD APK ============
def build_apk(url, app_name):
    info("Build APK butuh Android SDK + JDK 8+")
    print()
    warn("Kalau belum install:")
    print(f"{C_WHITE}    1. Android Studio: https://developer.android.com/studio")
    print(f"{C_WHITE}    2. JDK 8+: https://adoptium.net")
    print()

    confirm = prompt("Android SDK udah ke-install? (y/n)")
    if confirm.lower() != "y":
        info("Batal. Install dulu Android SDK, baru coba lagi.")
        press_enter()
        return

    android_home = os.environ.get("ANDROID_HOME", "")
    if not android_home or not os.path.isdir(android_home):
        err("ANDROID_HOME gak ke-set atau folder gak ada.")
        info("Set ANDROID_HOME ke folder SDK kamu, contoh:")
        print(f"{C_WHITE}    setx ANDROID_HOME \"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Android\\Sdk\"")
        press_enter()
        return

    out_dir = os.path.join(DOWNLOAD_DIR, app_name)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)

    info(f"Building APK dari: {url}")
    info(f"Output: {out_dir}")
    print()

    cwd_old = os.getcwd()
    os.chdir(out_dir)

    try:
        info("Init project...")
        subprocess.run("npx -y webapkify init", shell=True, timeout=120)

        config = f'''{{
  "appName": "{app_name}",
  "appId": "com.bara.{app_name.lower().replace(' ', '').replace('-', '')}",
  "version": "1.0.0",
  "url": "{url}"
}}'''
        with open("webapkify.config.ts", "w") as f:
            f.write(config)

        info("Build APK...")
        proc = subprocess.Popen(
            "npx -y webapkify build",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, shell=True, encoding="utf-8", errors="ignore"
        )
        for line in proc.stdout:
            print(f"{C_WHITE}  {line.rstrip()}")
        proc.wait()
    except Exception as e:
        err(f"Build gagal: {e}")
        os.chdir(cwd_old)
        press_enter()
        return
    finally:
        os.chdir(cwd_old)

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


# ============ ENTRY POINT ============
def web_builder():
    section("WEB BUILDER - Web to EXE / APK")

    # Cek Node.js
    node_ver = check_node()
    if not node_ver:
        err("Node.js belum keinstall.")
        info("Install: winget install OpenJS.NodeJS")
        info("Setelah install, TUTUP PowerShell → buka BARU.")
        press_enter()
        return

    npm_ver = check_npm()
    if not npm_ver:
        err("npm gak terdeteksi.")
        warn("Coba fix ini dulu di PowerShell:")
        print(f"{C_WHITE}    1. Tutup PowerShell, buka BARU")
        print(f"{C_WHITE}    2. Cek: npm --version")
        print(f"{C_WHITE}    3. Kalau masih error, cek PATH:")
        print(f"{C_WHITE}       $env:Path")
        press_enter()
        return

    ok(f"Node.js: {node_ver}")
    ok(f"npm    : v{npm_ver}")
    print()

    # Verifikasi URL
    url = prompt("Masukkan URL website (contoh: https://google.com)")
    if not url:
        err("URL kosong.")
        press_enter()
        return
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Nama app
    app_name = prompt("Nama app (contoh: MyApp)")
    if not app_name:
        err("Nama app kosong.")
        press_enter()
        return
    # Bersihin nama
    app_name = app_name.replace(" ", "").replace("-", "")

    # Pilih type
    print()
    print(f"  {C_YELLOW}[1]{C_WHITE} Web → EXE (Windows)")
    print(f"  {C_YELLOW}[2]{C_WHITE} Web → APK (Android — butuh Android SDK)")
    print()
    choice = prompt("Pilih [1/2]")

    if choice == "1":
        build_exe(url, app_name)
    elif choice == "2":
        build_apk(url, app_name)
    else:
        err("Pilihan gak valid.")

    press_enter()
