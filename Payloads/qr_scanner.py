from io import BytesIO

try:
    from PIL import Image
    from pyzbar.pyzbar import decode as qr_decode
except ImportError:
    Image, qr_decode = None, None

def scan_for_qr(image_bytes):
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
        pass # Not a valid image or no QR code
    return extracted_urls