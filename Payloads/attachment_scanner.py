import hashlib

try:
    from oletools.olevba import VBA_Parser
except ImportError:
    VBA_Parser = None

def scan_attachment(filename, file_bytes):
    print(f"\n[*] Analyzing Attachment: {filename}")
    
    # 1. Hash the file
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    print(f"    [*] SHA-256: {file_hash}")

    # 2. Extract Macros
    if VBA_Parser and filename.endswith(('.docm', '.xlsm', '.doc', '.xls')):
        try:
            vbaparser = VBA_Parser(filename, data=file_bytes)
            if vbaparser.detect_vba_macros():
                print("    [!] WARNING: VBA Macros found!")
                for (_, _, _, vba_code) in vbaparser.extract_macros():
                    if "Shell" in vba_code or "powershell" in vba_code.lower():
                        print("    [!] CRITICAL: Macro contains execution commands!")
            else:
                print("    [+] No macros detected.")
        except Exception as e:
            print(f"    [-] Macro scan failed: {e}")