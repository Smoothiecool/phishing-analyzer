import dns.resolver

def check_blacklist(domain):
    print(f"\n[*] Checking DNS Blacklists for MX servers of {domain}...")
    try:
        # First, find the MX records
        mx_answers = dns.resolver.resolve(domain, 'MX')
        for mx in mx_answers:
            mx_server = mx.exchange.to_text().rstrip('.')
            # Then, find the IP of the MX server
            ip_answers = dns.resolver.resolve(mx_server, 'A')
            
            for ip in ip_answers:
                ip_str = ip.to_text()
                reversed_ip = '.'.join(reversed(ip_str.split('.')))
                query = f"{reversed_ip}.zen.spamhaus.org"
                
                try:
                    dns.resolver.resolve(query, 'A')
                    print(f"    [!] WARNING: IP {ip_str} is BLACKLISTED on Spamhaus!")
                except dns.resolver.NXDOMAIN:
                    print(f"    [+] IP {ip_str} is clean.")
    except Exception as e:
        print(f"    [-] Could not complete blacklist check: {e}")