from twilio.rest import Client

account_sid = "YOUR_SID"
auth_token = "YOUR_TOKEN"

client = Client(account_sid, auth_token)

def send_whatsapp(to, message):
    client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=f'whatsapp:{to}'
    )