import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject="Your Credentials DID Document", body=None, to_email=None):
    # Email configuration
    sender_email = 'optisyncenablers@gmail.com'  # Your Gmail address
    sender_password = 'Optisync@3812'  # Your Gmail password

    # Create the MIME object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server (in this case, Gmail's SMTP server)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Enable TLS
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
