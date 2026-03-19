import argparse
import email
from email import policy
import dns.resolver

# Import our custom modules
from core.spf_dmarc_scanner import check_spf_dmarc
from core.ssl_scanner import check_ssl
from core.dns_blacklist_scanner import check_blacklist
from payloads.qr_scanner import scan_for_qr
from payloads.attachment_scanner import scan_attachment
from payloads.link_router import trace_url
from ai.nlp_analyzer import analyze_semantics

def run_domain_scan(domain):
    print(f"=== INFRASTRUCTURE SCAN: {domain} ===")
    check_spf_dmarc(domain)
    check_blacklist(domain)
    
    # Grab the primary MX to check SSL
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        if answers:
            primary_mx = answers[0].exchange.to_text().rstrip('.')
            check_ssl(primary_mx)
    except Exception:
        print("    [-] Could not resolve MX for SSL check.")

def run_file_scan(filepath):
    print(f"=== PAYLOAD SCAN: {filepath} ===")
    try:
        with open(filepath, 'rb') as f:
            msg = email.message_from_binary_file(f, policy=policy.default)
    except Exception as e:
        print(f"Error opening file: {e}")
        return

    body = ""
    for part in msg.walk():
        content_type = part.get_content_type()
        disposition = str(part.get("Content-Disposition"))

        # 1. Extract Body for AI
        if content_type in ["text/plain", "text/html"] and "attachment" not in disposition:
            body += str(part.get_content())
        
        # 2. Attachments & Macros
        if "attachment" in disposition or part.get_filename():
            scan_attachment(part.get_filename(), part.get_payload(decode=True))
        
        # 3. QR Codes
        if "image" in content_type:
            scan_for_qr(part.get_payload(decode=True))

    # 4. AI Semantics
    analyze_semantics(body)

    # 5. Extract and Route Links
    import re
    urls = list(set(re.findall(r'(https?://[^\s"\'<>]+)', body)))
    if urls:
        print(f"\n[*] Found {len(urls)} URLs. Routing...")
        for u in urls:
            trace_url(u)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Phishing Analysis Tool")
    parser.add_argument("-d", "--domain", help="Target domain for infrastructure check (e.g., example.com)")
    parser.add_argument("-f", "--file", help="Path to .eml file for payload analysis")

    args = parser.parse_args()

    if args.domain:
        run_domain_scan(args.domain)
    elif args.file:
        run_file_scan(args.file)
    else:
        print("Please provide a domain (-d) or file (-f). Use -h for help.")