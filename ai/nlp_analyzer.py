import re

try:
    from transformers import pipeline
    print("[*] Loading NLP Model...")
    classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")
except Exception:
    classifier = None

def analyze_semantics(text_body):
    if not classifier or not text_body.strip():
        return
    
    print("\n[*] Running AI Semantic Analysis...")
    # Clean HTML and truncate to 512 characters for the model
    clean_text = re.sub(r'<[^>]+>', '', text_body)[:512]
    
    try:
        result = classifier(clean_text)[0]
        score = round(result['score'] * 100, 2)
        
        if result['label'] == 'LABEL_1': 
            print(f"    [!] AI DANGER: {score}% probability of Phishing/Spam.")
        else:
            print(f"    [+] AI Assessment: {score}% probability of being Safe/Ham.")
    except Exception as e:
        print(f"    [-] AI Analysis failed: {e}")