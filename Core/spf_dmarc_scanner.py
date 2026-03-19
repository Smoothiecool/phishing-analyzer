import dns.resolver

def check_spf_dmarc(domain):
    print(f"\n[*] Checking SPF and DMARC for: {domain}")
    results = {"spf": "Missing", "dmarc": "Missing"}
    
    try:
        for rdata in dns.resolver.resolve(domain, 'TXT'):
            txt = rdata.to_text().strip('"')
            if txt.startswith('v=spf1'):
                results['spf'] = txt
                print(f"    [+] SPF: {txt}")
    except Exception:
        print("    [-] No SPF record found.")

    try:
        for rdata in dns.resolver.resolve(f"_dmarc.{domain}", 'TXT'):
            txt = rdata.to_text().strip('"')
            if txt.startswith('v=DMARC1'):
                results['dmarc'] = txt
                print(f"    [+] DMARC: {txt}")
    except Exception:
        print("    [-] No DMARC record found.")
        
    return results