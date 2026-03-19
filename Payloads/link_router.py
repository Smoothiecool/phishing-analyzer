import requests

def trace_url(url):
    print(f"\n[*] Tracing Route for: {url}")
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        final_url = response.url
        if final_url != url:
            print(f"    [!] REDIRECT: {url} -> {final_url}")
        else:
            print("    [+] No redirects detected.")
        return final_url
    except Exception as e:
        print(f"    [-] Error tracing link: {e}")
        return url