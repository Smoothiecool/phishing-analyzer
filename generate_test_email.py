import os
import requests
from email.message import EmailMessage

def build_phish_email():
    print("[*] Generating synthetic phishing email...")
    
    # 1. Initialize the Email Structure
    msg = EmailMessage()
    msg['Subject'] = "URGENT: Action Required - Account Suspended"
    msg['From'] = "Security Team <security@banc-update-secure.com>"
    msg['To'] = "victim@example.com"
    msg['Reply-To'] = "attacker-dropbox@gmail.com"

    # 2. Add the Text Body (Packed with NLP triggers and a deep link)
    body = """Dear User,

We have detected unauthorized login attempts on your account. 
Your account has been SUSPENDED pending immediate verification. 

Please review the attached invoice and verify your identity using the QR code below. 
If you do not complete this verification within 24 hours, your account will be permanently deleted.

You can also use this secure link: 
http://bit.ly/3JZTc5a

Thank you,
IT Security"""
    msg.set_content(body)

    # 3. Generate and Attach a Real QR Code (Quishing Payload)
    print("    [+] Fetching live QR code payload...")
    qr_data = "https://example.com/fake-login-page"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={qr_data}"
    
    try:
        response = requests.get(qr_url)
        if response.status_code == 200:
            msg.add_attachment(response.content, maintype='image', subtype='png', filename='verify_auth.png')
            print("    [+] QR Code attached successfully.")
    except Exception as e:
        print(f"    [-] Failed to fetch QR code: {e}")

    # 4. Attach a dummy file (to test the hashing mechanism)
    dummy_file_content = b"This is a fake attachment to test SHA-256 hashing."
    msg.add_attachment(dummy_file_content, maintype='application', subtype='octet-stream', filename='invoice_overdue.pdf')

    # 5. Save the final .eml file
    output_path = "test_payload.eml"
    with open(output_path, 'wb') as f:
        f.write(bytes(msg))
    
    print(f"\n[SUCCESS] Synthetic email saved to: {output_path}")
    print("You can now run: python main.py -f test_payload.eml")

if __name__ == "__main__":
    build_phish_email()