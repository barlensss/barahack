# ============================================================
#   BARA HACK TOOL - SAFELINK BYPASSER v2
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
    r"var\s+url\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",
    r"var\s+link\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",
    r"var\s+target\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",
    r"var\s+redirect\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",
    r"var\s+destination\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",
    r"var\s+dest\s*=\s*['\"]([a-zA-Z0-9+/=]{20,})['\"]",

    # URL langsung dalam JS
    r"var\s+url\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"var\s+link\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"var\s+target\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"window\.location\.href\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"location\.href\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"window\.location\s*=\s*['\"](https?://[^'\"]+)['\"]",
    r"window\.open\s*\(\s*['\"](https?://[^'\"]+)['\"]",

    # Meta refresh
    r'<meta\s+http-equiv=["\']refresh["\']\s+content=["\']\d+;\s*url=([^"\']+)["\']',
    r'<meta\s+http-equiv=["\']refresh["\']\s+content=["\']\d+;\s*URL=([^"\']+)["\']',

    # Anchor tag dengan teks "Get Link" / "Download"
    r'<a[^>]+href=["\'](https?://[^"\']+)["\'][^>]*>\s*(?:Get\s*Link|Download|Lanjut|Continue|Klik|Click)',
    
    # data-url / data-href
    r'data-url=["\'](https?://[^"\']+)["\']',
    r'data-href=["\'](https?://[^"\']+)["\']',
    r'data-target=["\'](https?://[^"\']+)["\']',
    r'data-redirect=["\'](https?://[^"\']+)["\']',
    r'data-link=["\'](https?://[^"\']+)["\']',
    
    # JSON
    r'"url"\s*:\s*"(https?://[^"]+)"',
    r'"link"\s*:\s*"(https?://[^"]+)"',
    r'"target"\s*:\s*"(https?://[^"]+)"',
    r'"redirect"\s*:\s*"(https?://[^"]+)"',
    r'"destination"\s*:\s*"(https?://[^"]+)"',
    
    # Onclick handler
    r'onclick=["\'][^"\']*?location\.(?:href\s*=\s*)?[\'"](https?://[^\'"]+)[\'"]',
    
    # Form action
    r'<form[^>]+action=["\'](https?://[^"\']+)["\']',
]

# Domain yang harus di-skip (bukan link tujuan)
SKIP_DOMAINS = [
    "safelinku.com", "sfl.gl", "safelink.me", "safelinkconverter",
    "google.com", "googleapis.com", "gstatic.com", "googletagmanager",
    "facebook.com", "fbcdn.net", "fb.com",
    "cloudflare.com", "cloudflareinsights.com", "cloudflare.net",
    "doubleclick.net", "googlesyndication.com", "google-analytics",
    "jquery.com", "bootstrapcdn.com", "fontawesome",
    "w3.org", "schema.org", "json-ld",
    "twitter.com", "instagram.com", "youtube.com/embed",
    "histats.com", "statcounter.com", "disqus.com",
]


def is_skip(url):
    """Cek apakah URL harus di-skip (bukan link tujuan)."""
    if not url:
        return True
    url_lower = url.lower()
    
    # Skip domain
    for domain in SKIP_DOMAINS:
        if domain in url_lower:
            return True
    
    # Skip file statis
    if any(url_lower.endswith(ext) for ext in
           [".js", ".css", ".png", ".jpg", ".jpeg", ".gif",
            ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot",
            ".webp", ".mp4", ".mp3", ".wav"]):
        return True
    
    # Skip URL sendiri (safelink)
    if "sfl.gl" in url_lower or "safelinku" in url_lower:
        return True
    
    return False


def try_b64_decode(s):
    """Coba decode base64, kalau valid return, kalau gak return None."""
    try:
        s_pad = s + "=" * (-len(s) % 4)
        decoded = base64.b64decode(s_pad).decode("utf-8", errors="ignore")
        if decoded.startswith("http"):
            return decoded
    except Exception:
        pass
    return None


def extract_links(html, source_url=""):
    """Ekstrak semua kemungkinan link tujuan dari HTML."""
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
            
            # Skip url sendiri
            if source_url and m == source_url:
                continue
            
            # Coba decode base64
            b64 = try_b64_decode(m)
            if b64:
                if not is_skip(b64) and b64 != source_url:
                    found.add(b64)
                continue
            
            # Coba URL decode
            try:
                decoded = urllib.parse.unquote(m)
                if decoded.startswith("http") and not is_skip(decoded) and decoded != source_url:
                    found.add(decoded)
            except Exception:
                pass
            
            # Langsung URL
            if m.startswith("http") and not is_skip(m) and m != source_url:
                found.add(m)
    
    return list(found)


def fetch_and_extract(url):
    """Fetch URL dan ekstrak link tujuan."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        final_url = r.url  # URL setelah redirect
        
        if r.status_code != 200:
            err(f"HTTP {r.status_code}")
            return None, []
        
        html = r.text
        
        # Kalau ada redirect langsung ke link tujuan
        if final_url != url and not is_skip(final_url):
            info(f"Redirect terdeteksi: {final_url}")
        
        links = extract_links(html, source_url=url)
        return final_url, links
    except Exception as e:
        err(f"Fetch error: {e}")
        return None, []


def bypass_safelink():
    """Fungsi utama — dipanggil dari main.py."""
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
    
    print()
    warn(f"Target: {url}")
    info("Proses: fetch HTML → parse → ekstrak link tujuan")
    print()
    confirm = prompt("Lanjut bypass? (y/n)")
    
    if confirm.lower() != "y":
        info("Dibatalkan.")
        press_enter()
        return
    
    print()
    info(f"Fetching: {url}")
    loading_bar("Bypass")
    
    final_url, links = fetch_and_extract(url)
    
    print()
    
    # Kalau ada redirect langsung
    if final_url and final_url != url and not is_skip(final_url):
        print(f"{C_GREEN}  [✓] Redirect langsung ke:")
        print(f"{C_YELLOW}      {final_url}\n")
    
    # Kalau ada link hasil parse
    if links:
        print(f"{C_GREEN}  [✓] Ketemu {len(links)} link kandidat:\n")
        for i, link in enumerate(links, 1):
            print(f"{C_WHITE}    [{i}] {C_YELLOW}{link}")
        
        # Ambil link pertama
        result = links[0]
        
        print(f"\n{C_GREEN}  ╔══════════════════════════════════════════════╗")
        print(f"{C_GREEN}  ║  {C_YELLOW}🔥 BYPASS BERHASIL! 🔥{C_GREEN}                       ║")
        print(f"{C_GREEN}  ╚══════════════════════════════════════════════╝\n")
        print(f"{C_WHITE}  Link asli: {C_YELLOW}{result}\n")
        
        # Tanya buka browser
        open_b = prompt("Buka di browser? (y/n)")
        if open_b.lower() == "y":
            import webbrowser
            webbrowser.open(result)
            ok("Dibuka di browser.")
    
    elif final_url and final_url != url and not is_skip(final_url):
        # Pakai redirect URL
        result = final_url
        
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
        print(f"{C_WHITE}    • Safelink pakai JavaScript obfuscation")
        print(f"{C_WHITE}    • Butuh timer + form POST")
        print(f"{C_WHITE}    • Pakai CAPTCHA / Cloudflare")
        print(f"{C_WHITE}    • Butuh klik manual di browser")
        print()
        info("Coba buka manual: " + url)
        
        open_b = prompt("Buka di browser? (y/n)")
        if open_b.lower() == "y":
            import webbrowser
            webbrowser.open(url)
    
    press_enter()
