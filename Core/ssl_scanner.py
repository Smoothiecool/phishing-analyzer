import socket
import ssl

def check_ssl(mx_server):
    print(f"\n[*] Checking SSL/TLS on {mx_server}...")
    context = ssl.create_default_context()
    try:
        with socket.create_connection((mx_server, 465), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=mx_server) as ssock:
                cert = ssock.getpeercert()
                print("    [+] SSL Certificate is VALID.")
                print(f"    [+] Issuer: {cert['issuer'][1][0][1]}")
                return True
    except Exception as e:
        print(f"    [-] SSL Error or port 465 closed: {e}")
        return False