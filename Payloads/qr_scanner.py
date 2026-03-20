from io import BytesIO

# We use a broad 'Exception' here to catch the missing Windows DLL error
try:
    from PIL import Image
    from pyzbar.pyzbar import decode as qr_decode
except Exception as e:
    print("    [!] QR Scanner disabled: Missing Windows C++ dependencies. Skipping QR scan.")
    Image, qr_decode = None, None

def scan_for_qr(image_bytes):
    # If the libraries didn't load, just return an empty list and move on
    if not Image or not qr_decode:
        return []
    
    extracted_urls = []
    try:
        img = Image.open(BytesIO(image_bytes))
        decoded_objects = qr_decode(img)
        for obj in decoded_objects:
            hidden_url = obj.data.decode("utf-8")
            print(f"    [!] QUISHING ALERT: QR Code detected pointing to: {hidden_url}")
            extracted_urls.append(hidden_url)
    except Exception:
        pass # Not a valid image or no QR code found
        
    return extracted_urls