import requests
from .models import ActivityLog
def send_smis(otp, phone):
    
    api_url = "https://sms.arkesel.com/sms/api"
    api_key = "Y21uY0ZmR2dUZmtRb3dNSGRQcmc"



    sms_string = f"Your OTP is - \n {otp} \nEnter this code to initiate your order. \nDo not share this code with anyone. \n\nIf you did not initiate this order, please ignore this message."




  
    payload = {
        'action': 'send-sms',
        'api_key': api_key,
        'to': phone,
        'from': 'O2Citi',
        'sms': sms_string
    }
    
    try:
        response = requests.get(api_url, params=payload)
        response.raise_for_status()
        
        print(response.text)
        ActivityLog.objects.create(activity=f"SMS sent successfully: {response.text}")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
   
import requests

def send_sms(phone):
    client = requests.Session()

    headers = {
        "api-key": "Y21uY0ZmR2dUZmtRb3dNSGRQcmc"
    }

    url = "https://sms.arkesel.com/api/otp/generate"

    request_body = {
        "expiry": "5",
        "length": "6",
        "medium": "sms",
        "message": "Your OTP is - %otp_code% Enter this code to initiate your order",
        "number": phone,
        "sender_id": "O2Citi",
        "type": "numeric"
    }

    try:
        response = client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        print(f"{response.json()}")
        return response.json().get('code')
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None


