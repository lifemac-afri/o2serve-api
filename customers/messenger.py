import requests
from .models import ActivityLog
def send_sms(otp, phone):
    
    sms_string = ( f'''O2Citi Confirmation

Your one-time password (OTP) is {otp}. Enter this code to confirm your order.
This OTP is valid for 10 minutes. Do not share this code with anyone.

If you did not initiate this order, please ignore this message.''')

    api_key = "435|SrJE2ycHmmOLkfmGsByYLkdqsfuDVHHtf5MhCkUF"
    api_url = "https://www.webapp.usmsgh.com/api/sms/send"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "recipient": phone,
        "sender_id": "Eugene.Dev",
        "message": sms_string
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        # Create a log of whatever happens
        ActivityLog.objects.create(activity=f"SMS sent successfully: {response.json()}")
        print("SMS sent successfully:", response.json())
    except requests.RequestException as e:
        print("Failed to send SMS:", str(e))
