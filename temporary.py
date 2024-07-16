import requests
import random
import string
from datetime import datetime
import re

def generate_random_email():
    """Generate random email"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    prefix_length = 8
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=prefix_length))
    domain = 'qabq'
    email = f"{prefix}@{domain}.com"
    return email

def get_authorization_token():
    """Get authorize token"""
    url = "https://api.mail.cx/api/v1/auth/authorize_token"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer undefined"
    }
    data = {}
    response = requests.post(url, headers=headers, json=data)
    token = response.json()
    return token

def fetch_verification_code(email, token):
    """Get token from random email"""
    # Get email list
    url = f"https://api.mail.cx/api/v1/mailbox/{email}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    # Find the code mail
    verification_code = None
    for item in response.json():
        if "CDP Identity PRD account email verification code" in item.get("subject", ""):
            email_id = item.get("id")
            url = f"https://api.mail.cx/api/v1/mailbox/{email}/{email_id}"
            response = requests.get(url, headers=headers)
            text = response.text
            match = re.search(r"Your code is: (\d+)", text)
            if match:
                verification_code = match.group(1)
                break
    
    return verification_code
