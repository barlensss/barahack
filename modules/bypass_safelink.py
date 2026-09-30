# ============================================================
#   BARA HACK TOOL - SAFELINK BYPASSER
#   Created by BARA
#   Bypass SafelinkU / shortlink ads → link asli
# ============================================================

import re
import base64
import urllib.parse
import requests
from ui import (section, prompt, err, info, warn, ok, press_enter,
                loading_bar, C_WHITE, C_YELLOW, C_GREEN, C_RED, C_CYAN)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
}


# ============ PATTERN BYPASS ============
PATTERNS = [
    # Base64 dalam JS variable
    r"var\s+url\s*=\s*['\"]([a-zA-Z0-9+/=]+)['\"]",
    r"var\s+link\s*=\s*['\"]([a-zA-Z0-9+/=]+)['\"]",
    r"var\s+target\s*=\s*['\"]([a-zA-Z0-9+/=]+)['\"]",
    r"var\s+redirect\s*=\s*['\"]([a-zA-Z0-9+/=]+)['\"]",

    # URL langsung dalam JS
    r"var\s+url\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"var\s+link\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"window\.location\.href\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"location\.href\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"window\.location\s*=\s*['\"](https?://[^'\"]+)['\"]",

    # Meta refresh
    r'<meta\s+http-equiv=["\']refresh["\']\s+content=["\']\d+;\s*url=([^"\']+)["\']',
    r'<meta\s+http-equiv=["\']refresh["\']\s+content=["\']\d+;\s*URL=([^"\']+)["\']',

    # Anchor tag
    r'<a[^>]+href=["\'](https?://[^"\']+)["\'][^>]*>',
    
    # data-url / data-href
    r'data-url=["\'](https?://[^"\']+)["\']',
    r'data-href=["\'](https?://[^"\']+)["\']',
    r'data-target=["\'](https?://[^"\']+)["\']',
    
    # JSON
    r'"url"\s*:\s*"(https?://[^"]+)"',
    r'"link"\s*:\s*"(https?://[^"]+)"',
    r'"target"\s*:\s*"(https?://[^"]+)"',
    r'"redirect"\s*:\s*"(https?://[^"]+)"',
    
    # Onclick handler
    r'onclick=["\']window\.location\s*=\s*[\'"](https?://[^\'"]+)[\'"]',
    r'onclick=["\']location\.href\s*=\s*[\'"](https?://[^\'"]+)[\'"]',
]

# Domain yang harus di-skip (bukan link tujuan)
SKIP_DOMAINS = [
    "safelinku.com", "sfl.gl", "safelink.me",
    "google.com", "googleapis.com", "gstatic.com",
    "facebook.com", "fbcdn.net",
    "cloudflare.com", "cloudflareinsights.com",
    "doubleclick.net", "googlesyndication.com",
    "jquery.com", "bootstrapcdn.com",
    "safelinkconverter.com", "shortlink",
]


def is_skip(url):
    """Cek apakah URL harus di-skip (bukan link tujuan)."""
    if not url:
        return True
    url_lower = url.lower()
    for domain in SKIP_DOMAINS:
        if domain in url_lower:
            return True
    # Skip url statis
    if any(url_lower.endswith(ext) for ext in 
           [".js", ".css", ".png", ".jpg", ".jpeg", ".gif", 
            ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot"]):
        return True
    return False


def try_b64_decode(s):
    """Coba decode base64, kalau valid return, kalau gak return None."""
    try:
        # Tambah padding kalau kurang
        s_pad = s + "=" * (-len(s) % 4)
        decoded = base64.b64decode(s_pad).decode("utf-8", errors="ignore")
        if decoded.startswith("http"):
            return decoded
    except Exception:
        pass
    return None


def extract_links(html):
    """Ekstrak semua kemungkinan link tujuan dari HTML."""
    found = set()
    
    for pattern in PATTERNS:
        matches = re.findall(pattern, html, re.IGNORECASE)
        for m in matches:
            m = m.strip()
            
            # Coba decode base64
            b64 = try_b64_decode(m)
            if b64:
                if not is_skip(b64):
                    found.add(b64)
                continue
            
            # Coba URL decode
            try:
                decoded = urllib.parse.unquote(m)
                if decoded.startswith("http") and not is_skip(decoded):
                    found.add(decoded)
            except Exception:
                pass
            
            # Langsung URL
            if m.startswith("http") and not is_skip(m):
                found.add(m)
    
    return list(found)


def bypass_safelink(url):
    """Bypass 1 URL safelink."""
    info(f"Target: {url}")
    loading_bar("Fetching")
    
    try:
        r = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
    except Exception as e:
        err(f"Gagal fetch: {e}")
        return None
    
    if r.status_code != 200:
        err(f"HTTP {r.status_code}")
        return None
    
    html = r.text
    info(f"Ukuran HTML: {len(html):,} bytes")
    
    # Ekstrak links
    links = extract_links(html)
    
    if not links:
        warn("Gak ada link ditemukan di HTML.")
        return None
    
    print(f"\n{C_GREEN}  [✓] Ketemu {len(links)} link kandidat:\n")
    for i, link in enumerate(links, 1):
        print(f"{C_WHITE}    [{i}] {C_YELLOW}{link}")
    
    return links[0]  # Ambil yang pertama


def bypass_safelink():
    section("BYPASS SAFELINKU")
    info("Bypass link safelink / shortlink ads")
    print()
    
    url = prompt("Masukkan URL safelink")
    if not url:
        err("URL kosong.")
        press_enter()
        return
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    # Konfirmasi
    print()
    warn(f"Bypass: {url}")
    warn("Proses: fetch HTML → parse → ekstrak link tujuan")
    print()
    confirm = prompt("Lanjut bypass? (y/n)")
    
    if confirm.lower() != "y":
        info("Dibatalkan.")
        press_enter()
        return
    
    print()
    result = bypass_safelink(url)
    
    if result:
        print(f"\n{C_GREEN}  ╔══════════════════════════════════════════════╗")
        print(f"{C_GREEN}  ║  {C_YELLOW}🔥 BYPASS BERHASIL! 🔥{C_GREEN}                       ║")
        print(f"{C_GREEN}  ╚══════════════════════════════════════════════╝\n")
        print(f"{C_WHITE}  Link asli: {C_YELLOW}{result}\n")
        
        # Tanya mau buka di browser?
        open_browser = prompt("Buka di browser? (y/n)")
        if open_browser.lower() == "y":
            import webbrowser
            webbrowser.open(result)
            ok("Dibuka di browser.")
    else:
        err("Gagal bypass. Coba cek manual atau pakai tool lain.")
    
    press_enter()
