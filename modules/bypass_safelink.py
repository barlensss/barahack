# ============================================================
#   BARA HACK TOOL - SAFELINK BYPASSER v3
#   Created by BARA
#   Pakai Selenium — bypass safelink pakai timer + button
# ============================================================

import re
import time
import base64
import urllib.parse
import requests
from ui import (section, prompt, err, info, warn, ok, press_enter,
                loading_bar, C_WHITE, C_YELLOW, C_GREEN, C_RED, C_CYAN)


# ============ CEK SELENIUM ============
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_OK = True
except ImportError:
    SELENIUM_OK = False


# ============ PATTERN BYPASS (FALLBACK) ============
PATTERNS = [
    r"var\s+url\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",
    r"var\s+link\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",
    r"var\s+target\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",
    r"var\s+redirect\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",
    r"var\s+destination\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",
    r"var\s+url\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"var\s+link\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"window\.location\.href\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"location\.href\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"window\.open\s*\(\s*['\"](https?://[^'\"]+)['\"]",
    r'<meta\s+http-equiv=["\']refresh["\']\s+content=["\']\d+;\s*url=([^"\']+)["\']',
    r'data-url=["\'](https?://[^"\']+)["\']',
    r'data-href=["\'](https?://[^"\']+)["\']',
    r'"url"\s*:\s*"(https?://[^"]+)"',
    r'"link"\s*:\s*"(https?://[^"]+)"',
]

SKIP_DOMAINS = [
    "safelinku.com", "sfl.gl", "safelink.me",
    "google.com", "googleapis.com", "gstatic.com", "googletagmanager",
    "facebook.com", "fbcdn.net", "fb.com",
    "cloudflare.com", "cloudflareinsights.com",
    "doubleclick.net", "googlesyndication.com",
    "jquery.com", "bootstrapcdn.com",
]


def is_skip(url, source_url=""):
    if not url:
        return True
    if source_url and url == source_url:
        return True
    url_lower = url.lower()
    for domain in SKIP_DOMAINS:
        if domain in url_lower:
            return True
    if any(url_lower.endswith(ext) for ext in
           [".js", ".css", ".png", ".jpg", ".jpeg", ".gif",
            ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot"]):
        return True
    return False


def try_b64_decode(s):
    try:
        s_pad = s + "=" * (-len(s) % 4)
        decoded = base64.b64decode(s_pad).decode("utf-8", errors="ignore")
        if decoded.startswith("http"):
            return decoded
    except Exception:
        pass
    return None


def extract_links(html, source_url=""):
    """Ekstrak link dari HTML (fallback kalau selenium gagal)."""
    found = set()
    for pattern in PATTERNS:
        try:
            matches = re.findall(pattern, html, re.IGNORECASE)
        except Exception:
            continue
        for m in matches:
            if not m or not isinstance(m, str):
                continue
            m = m.strip()
            b64 = try_b64_decode(m)
            if b64 and not is_skip(b64, source_url):
                found.add(b64)
                continue
            try:
                decoded = urllib.parse.unquote(m)
                if decoded.startswith("http") and not is_skip(decoded, source_url):
                    found.add(decoded)
            except Exception:
                pass
            if m.startswith("http") and not is_skip(m, source_url):
                found.add(m)
    return list(found)


# ============ SELENIUM BYPASS ============
def selenium_bypass(url):
    """Bypass pakai headless Chrome."""
    info("Menjalankan headless Chrome...")
    print()

    # Setup Chrome headless
    opts = Options()
    opts.add_argument("--headless=new")           # headless baru
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--log-level=3")            # cuma error
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    driver = None
    try:
        info("Setup chromedriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
        driver.set_page_load_timeout(30)

        # Buka URL
        info(f"Membuka: {url}")
        driver.get(url)

        # Tunggu load
        time.sleep(3)

        original_url = url
        final_url = driver.current_url
        
        # Loop: tunggu 20 detik, cek redirect
        max_wait = 25
        start = time.time()
        
        while time.time() - start < max_wait:
            current = driver.current_url
            
            # Kalau URL berubah (redirect otomatis)
            if current != original_url and not is_skip(current, original_url):
                info(f"Redirect otomatis: {current}")
                final_url = current
                break
            
            # Cari button "Get Link" / "Download" / dll
            try:
                buttons = driver.find_elements(By.XPATH, 
                    "//*[contains(translate(text(), 'GETLINKDOWNLOADCONTINUELANJUTKLIK', "
                    "'getlinkdownloadcontinuclanjutklik'), 'getlink') "
                    "or contains(translate(text(), 'GETLINKDOWNLOADCONTINUELANJUTKLIK', "
                    "'getlinkdownloadcontinuclanjutklik'), 'download') "
                    "or contains(translate(text(), 'GETLINKDOWNLOADCONTINUELANJUTKLIK', "
                    "'getlinkdownloadcontinuclanjutklik'), 'continue') "
                    "or contains(translate(text(), 'GETLINKDOWNLOADCONTINUELANJUTKLIK', "
                    "'getlinkdownloadcontinuclanjutklik'), 'lanjut')]"
                )
                
                for btn in buttons:
                    try:
                        if btn.is_displayed() and btn.is_enabled():
                            driver.execute_script("arguments[0].click();", btn)
                            info(f"Klik button: {btn.text[:30]}")
                            time.sleep(2)
                            break
                    except Exception:
                        continue
            except Exception:
                pass
            
            time.sleep(1)
        
        # Ambil URL final
        final_url = driver.current_url
        page_source = driver.page_source
        
        # Cari link di page source juga (untuk jaga-jaga)
        links_in_html = extract_links(page_source, source_url=original_url)
        
        return final_url, links_in_html
    
    except Exception as e:
        err(f"Selenium error: {e}")
        return None, []
    
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


def requests_bypass(url):
    """Fallback: bypass pakai requests biasa."""
    try:
        r = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }, timeout=15, allow_redirects=True)
        
        final_url = r.url
        links = extract_links(r.text, source_url=url)
        return final_url, links
    except Exception as e:
        err(f"Requests error: {e}")
        return None, []


# ============ FUNGSI UTAMA ============
def bypass_safelink():
    section("BYPASS SAFELINKU")
    info("Bypass link safelink / shortlink ads")
    
    if not SELENIUM_OK:
        print()
        warn("Selenium belum keinstall!")
        print(f"{C_WHITE}    Install dulu:")
        print(f"{C_YELLOW}    pip install selenium webdriver-manager")
        print()
        info("Kalau gak mau install Selenium, pakai mode 'requests' (kurang akurat).")
        print()
        mode = prompt("Pakai mode requests aja? (y/n)")
        if mode.lower() != "y":
            press_enter()
            return
        use_selenium = False
    else:
        use_selenium = True
    
    print()
    url = prompt("Masukkan URL safelink")
    if not url:
        err("URL kosong.")
        press_enter()
        return
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    print()
    warn(f"Target: {url}")
    if use_selenium:
        info("Mode: Selenium (headless Chrome) — tunggu 20-30 detik")
    else:
        info("Mode: requests (fallback)")
    print()
    confirm = prompt("Lanjut bypass? (y/n)")
    
    if confirm.lower() != "y":
        info("Dibatalkan.")
        press_enter()
        return
    
    print()
    loading_bar("Bypass")
    
    # Bypass
    if use_selenium:
        final_url, links = selenium_bypass(url)
    else:
        final_url, links = requests_bypass(url)
    
    print()
    
    # Hasil
    result = None
    
    # 1. Cek final URL
    if final_url and final_url != url and not is_skip(final_url, url):
        result = final_url
        print(f"{C_GREEN}  [✓] Final URL: {C_YELLOW}{final_url}\n")
    
    # 2. Cek links di HTML
    if links:
        print(f"{C_GREEN}  [✓] Ketemu {len(links)} link di HTML:\n")
        for i, link in enumerate(links, 1):
            print(f"{C_WHITE}    [{i}] {C_YELLOW}{link}")
        if not result:
            result = links[0]
        print()
    
    # Tampilkan hasil
    if result:
        print(f"{C_GREEN}  ╔══════════════════════════════════════════════╗")
        print(f"{C_GREEN}  ║  {C_YELLOW}🔥 BYPASS BERHASIL! 🔥{C_GREEN}                       ║")
        print(f"{C_GREEN}  ╚══════════════════════════════════════════════╝\n")
        print(f"{C_WHITE}  Link asli: {C_YELLOW}{result}\n")
        
        open_b = prompt("Buka di browser? (y/n)")
        if open_b.lower() == "y":
            import webbrowser
            webbrowser.open(result)
            ok("Dibuka di browser.")
    else:
        err("Gak ketemu link tujuan.")
        print()
        warn("Kemungkinan:")
        print(f"{C_WHITE}    • Butuh login / verifikasi manual")
        print(f"{C_WHITE}    • Pakai CAPTCHA")
        print(f"{C_WHITE}    • Cloudflare challenge")
        print(f"{C_WHITE}    • Timer lebih dari 30 detik")
        print()
        info("Coba buka manual: " + url)
        
        open_b = prompt("Buka di browser? (y/n)")
        if open_b.lower() == "y":
            import webbrowser
            webbrowser.open(url)
    
    press_enter()
