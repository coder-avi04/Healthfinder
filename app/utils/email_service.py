import smtplib
from email.mime.text import MIMEText

EMAIL = "ahmadanas6662@gmail.com"
PASSWORD = "uplz zbfd uciy foqn"  # 🔥 MUST be app password

def send_email(to_email, subject, message):
    try:
        print("📧 Sending email to:", to_email)

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        print("🔐 Logging in...")
        server.login(EMAIL, PASSWORD)

        print("📤 Sending message...")
        server.sendmail(EMAIL, to_email, msg.as_string())

        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ EMAIL ERROR:", e)