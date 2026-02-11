import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_reset_email(to_email: str, reset_link: str) -> bool:
    """Send password reset email. Uses SMTP settings from env vars.

    Returns True if an attempt to send was made, False if SMTP not configured.
    """
    host = os.environ.get("SMTP_HOST")
    port = os.environ.get("SMTP_PORT")
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")
    from_addr = os.environ.get("FROM_EMAIL", user)

    if not host or not port or not user or not password:
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = to_email
        msg["Subject"] = "Password reset for your Simple Tuition account"
        body = f"Use the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, ignore this email."
        msg.attach(MIMEText(body, "plain"))

        port_int = int(port)
        if port_int == 465:
            server = smtplib.SMTP_SSL(host, port_int)
        else:
            server = smtplib.SMTP(host, port_int)
            server.starttls()

        server.login(user, password)
        server.sendmail(from_addr, [to_email], msg.as_string())
        server.quit()
        return True
    except Exception:
        return False
